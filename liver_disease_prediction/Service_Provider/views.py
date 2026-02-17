from django.db.models import Count, Avg, Q
from django.shortcuts import render, redirect
from django.http import HttpResponse
import xlwt
import pandas as pd
import numpy as np
import os
import warnings

warnings.filterwarnings("ignore")

from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split

from Remote_User.models import (
    ClientRegister_Model,
    disease_prediction,
    detection_ratio,
    detection_accuracy
)

# =========================================================
# HELPER FUNCTION
# =========================================================
def apply_results(value):
    try:
        if float(value) > 0.5:
            return 1   # Liver Disease
        else:
            return 0   # No Liver Disease
    except:
        return 0


# =========================================================
# SERVICE PROVIDER LOGIN
# =========================================================
def serviceproviderlogin(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            if username.lower() == "admin" and password.lower() == "admin":
                return redirect('View_Remote_Users')
            else:
                return render(
                    request,
                    'SProvider/serviceproviderlogin.html',
                    {'error': 'Invalid Service Provider credentials'}
                )

    return render(request, 'SProvider/serviceproviderlogin.html')


# =========================================================
# VIEW REMOTE USERS
# =========================================================
def View_Remote_Users(request):
    obj = ClientRegister_Model.objects.all()
    return render(request, 'SProvider/View_Remote_Users.html', {'objects': obj})


# =========================================================
# VIEW LIVER DISEASE STATUS
# =========================================================
def View_Liver_Disease_Status(request):
    obj = disease_prediction.objects.all()
    return render(request, 'SProvider/View_Liver_Disease_Status.html', {'list_objects': obj})


# =========================================================
# FIND LIVER DISEASE RATIO
# =========================================================
def Find_Liver_Disease_Ratio(request):
    detection_ratio.objects.all().delete()

    total = disease_prediction.objects.count()
    if total == 0:
        return render(request, 'SProvider/Find_Liver_Disease_Ratio.html', {'objs': []})

    no_disease = disease_prediction.objects.filter(prediction="No Liver Disease").count()
    disease = disease_prediction.objects.filter(prediction="Found Liver Disease").count()

    detection_ratio.objects.create(
        names="No Liver Disease",
        ratio=(no_disease / total) * 100
    )

    detection_ratio.objects.create(
        names="Found Liver Disease",
        ratio=(disease / total) * 100
    )

    obj = detection_ratio.objects.all()
    return render(request, 'SProvider/Find_Liver_Disease_Ratio.html', {'objs': obj})


# =========================================================
# CHARTS
# =========================================================
def charts(request, chart_type):
    chart1 = detection_ratio.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, "SProvider/charts.html", {'form': chart1, 'chart_type': chart_type})


def charts1(request, chart_type):
    chart1 = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(request, "SProvider/charts1.html", {'form': chart1, 'chart_type': chart_type})


# =========================================================
# DOWNLOAD TRAINED DATA
# =========================================================
def Download_Trained_DataSets(request):
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="TrainedData.xls"'

    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet("Liver Data")

    headers = [
        "Pid", "Age", "Gender", "Total_Bilirubin", "Direct_Bilirubin",
        "Alkaline_Phosphotase", "Alamine_Aminotransferase",
        "Aspartate_Aminotransferase", "Total_Protiens",
        "Albumin", "Albumin_and_Globulin_Ratio", "Prediction"
    ]

    for col, header in enumerate(headers):
        ws.write(0, col, header)

    row = 1
    for obj in disease_prediction.objects.all():
        ws.write(row, 0, obj.Pid)
        ws.write(row, 1, obj.Age)
        ws.write(row, 2, obj.Gender)
        ws.write(row, 3, obj.Total_Bilirubin)
        ws.write(row, 4, obj.Direct_Bilirubin)
        ws.write(row, 5, obj.Alkaline_Phosphotase)
        ws.write(row, 6, obj.Alamine_Aminotransferase)
        ws.write(row, 7, obj.Aspartate_Aminotransferase)
        ws.write(row, 8, obj.Total_Protiens)
        ws.write(row, 9, obj.Albumin)
        ws.write(row, 10, obj.Albumin_and_Globulin_Ratio)
        ws.write(row, 11, obj.prediction)
        row += 1

    wb.save(response)
    return response


# =========================================================
# TRAIN & TEST DATASETS (FINAL FIXED VERSION)
# =========================================================
def Train_Test_DataSets(request):
    detection_accuracy.objects.all().delete()

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    dataset_path = os.path.join(BASE_DIR, 'liver_patient.csv')

    df = pd.read_csv(dataset_path)

    # Handle missing values
    df = df.fillna(df.mean(numeric_only=True))

    # Create target column
    df['Results'] = df['Direct_Bilirubin'].apply(apply_results)

    X = df[['Age', 'Total_Bilirubin', 'Direct_Bilirubin',
             'Alkaline_Phosphotase', 'Alamine_Aminotransferase',
             'Aspartate_Aminotransferase', 'Total_Protiens',
             'Albumin', 'Albumin_and_Globulin_Ratio']]

    y = df['Results']

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    models = {
        "SVM": svm.LinearSVC(),
        "Logistic Regression": LogisticRegression(max_iter=1000),
        "Random Forest": RandomForestClassifier(),
        "Decision Tree": DecisionTreeClassifier(),
        "KNN": KNeighborsClassifier()
    }

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        acc = accuracy_score(y_test, preds) * 100
        detection_accuracy.objects.create(names=name, ratio=acc)

    obj = detection_accuracy.objects.all()
    return render(request, 'SProvider/Train_Test_DataSets.html', {'objs': obj})


# =========================================================
# LIKE CHART
# =========================================================
def likeschart(request, like_chart):
    charts = detection_accuracy.objects.values('names').annotate(dcount=Avg('ratio'))
    return render(
        request,
        "SProvider/likeschart.html",
        {'form': charts, 'like_chart': like_chart}
    )
