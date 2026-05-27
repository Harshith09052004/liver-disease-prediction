from django.db.models import Count, Avg
from django.shortcuts import render, redirect
from django.db.models import Q
import pandas as pd
import warnings

warnings.filterwarnings("ignore")

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier

import xlwt
from django.http import HttpResponse

from Remote_User.models import (
    ClientRegister_Model,
    disease_prediction,
    detection_ratio,
    detection_accuracy
)


# SERVICE PROVIDER LOGIN
def serviceproviderlogin(request):

    if request.method == "POST":

        admin = request.POST.get('username')
        password = request.POST.get('password')

        if admin == "Admin" and password == "Admin":
            return redirect('View_Remote_Users')

    return render(request, 'SProvider/serviceproviderlogin.html')


# FIND LIVER DISEASE RATIO
def Find_Liver_Disease_Ratio(request):

    detection_ratio.objects.all().delete()

    # No Liver Disease
    kword = 'No Liver Disease'

    obj = disease_prediction.objects.all().filter(
        Q(prediction=kword)
    )

    obj1 = disease_prediction.objects.all()

    count = obj.count()
    count1 = obj1.count()

    ratio = (count / count1) * 100

    if ratio != 0:
        detection_ratio.objects.create(
            names=kword,
            ratio=ratio
        )

    # Found Liver Disease
    kword1 = 'Foud Liver Disease'

    obj1 = disease_prediction.objects.all().filter(
        Q(prediction=kword1)
    )

    obj11 = disease_prediction.objects.all()

    count1 = obj1.count()
    count11 = obj11.count()

    ratio1 = (count1 / count11) * 100

    if ratio1 != 0:
        detection_ratio.objects.create(
            names=kword1,
            ratio=ratio1
        )

    obj = detection_ratio.objects.all()

    return render(
        request,
        'SProvider/Find_Liver_Disease_Ratio.html',
        {'objs': obj}
    )


# VIEW REMOTE USERS
def View_Remote_Users(request):

    obj = ClientRegister_Model.objects.all()

    return render(
        request,
        'SProvider/View_Remote_Users.html',
        {'objects': obj}
    )


# VIEW TRENDINGS
def ViewTrendings(request):

    topic = disease_prediction.objects.values(
        'topics'
    ).annotate(
        dcount=Count('topics')
    ).order_by('-dcount')

    return render(
        request,
        'SProvider/ViewTrendings.html',
        {'objects': topic}
    )


# CHARTS
def charts(request, chart_type):

    chart1 = detection_ratio.objects.values(
        'names'
    ).annotate(
        dcount=Avg('ratio')
    )

    return render(
        request,
        "SProvider/charts.html",
        {
            'form': chart1,
            'chart_type': chart_type
        }
    )


def charts1(request, chart_type):

    chart1 = detection_accuracy.objects.values(
        'names'
    ).annotate(
        dcount=Avg('ratio')
    )

    return render(
        request,
        "SProvider/charts1.html",
        {
            'form': chart1,
            'chart_type': chart_type
        }
    )


# VIEW LIVER DISEASE STATUS
def View_Liver_Disease_Status(request):

    obj = disease_prediction.objects.all()

    return render(
        request,
        'SProvider/View_Liver_Disease_Status.html',
        {'list_objects': obj}
    )


# LIKE CHART
def likeschart(request, like_chart):

    charts = detection_accuracy.objects.values(
        'names'
    ).annotate(
        dcount=Avg('ratio')
    )

    return render(
        request,
        "SProvider/likeschart.html",
        {
            'form': charts,
            'like_chart': like_chart
        }
    )


# DOWNLOAD TRAINED DATASETS
def Download_Trained_DataSets(request):

    response = HttpResponse(
        content_type='application/ms-excel'
    )

    response[
        'Content-Disposition'
    ] = 'attachment; filename="TrainedData.xls"'

    wb = xlwt.Workbook(encoding='utf-8')

    ws = wb.add_sheet("sheet1")

    row_num = 0

    font_style = xlwt.XFStyle()
    font_style.font.bold = True

    obj = disease_prediction.objects.all()

    for my_row in obj:

        row_num = row_num + 1

        ws.write(row_num, 0, my_row.Pid, font_style)
        ws.write(row_num, 1, my_row.Age, font_style)
        ws.write(row_num, 2, my_row.Gender, font_style)
        ws.write(row_num, 3, my_row.Total_Bilirubin, font_style)
        ws.write(row_num, 4, my_row.Direct_Bilirubin, font_style)
        ws.write(row_num, 5, my_row.Alkaline_Phosphotase, font_style)
        ws.write(row_num, 6, my_row.Alamine_Aminotransferase, font_style)
        ws.write(row_num, 7, my_row.Aspartate_Aminotransferase, font_style)
        ws.write(row_num, 8, my_row.Total_Protiens, font_style)
        ws.write(row_num, 9, my_row.Albumin, font_style)
        ws.write(row_num, 10, my_row.Albumin_and_Globulin_Ratio, font_style)
        ws.write(row_num, 11, my_row.prediction, font_style)

    wb.save(response)

    return response


# TRAIN TEST DATASETS
def Train_Test_DataSets(request):

    detection_accuracy.objects.all().delete()

    # LOAD DATASET
    df = pd.read_csv('liver_patient.csv')

    # REMOVE NULL VALUES
    df.dropna(inplace=True)

    # TARGET VARIABLE
    def apply_results(results):

        if results <= 1.2 and results >= 0.1:
            return 0

        else:
            return 1

    df['Results'] = df['Direct_Bilirubin'].apply(
        apply_results
    )

    # CONVERT GENDER
    df['Gender'] = df['Gender'].map({
        'Male': 1,
        'Female': 0
    })

    # FEATURES
    X = df[[
        'Age',
        'Gender',
        'Total_Bilirubin',
        'Direct_Bilirubin',
        'Alkaline_Phosphotase',
        'Alamine_Aminotransferase',
        'Aspartate_Aminotransferase',
        'Total_Protiens',
        'Albumin',
        'Albumin_and_Globulin_Ratio'
    ]]

    # TARGET
    y = df['Results']

    # FEATURE SCALING
    scaler = StandardScaler()

    X = scaler.fit_transform(X)

    # SPLIT DATA
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42
    )

    # MODELS
    models = {

        "Naive Bayes": GaussianNB(),

        "SVM": SVC(),

        "Logistic Regression": LogisticRegression(
            max_iter=1000
        ),

        "Decision Tree Classifier": DecisionTreeClassifier(),

        "Random Forest Classifier": RandomForestClassifier(),

        "KNeighborsClassifier": KNeighborsClassifier()

    }

    # TRAIN MODELS
    for name, model in models.items():

        print("\n")
        print(name)

        model.fit(X_train, y_train)

        predictions = model.predict(X_test)

        accuracy = accuracy_score(
            y_test,
            predictions
        ) * 100

        print("ACCURACY")
        print(accuracy)

        print("CLASSIFICATION REPORT")
        print(
            classification_report(
                y_test,
                predictions
            )
        )

        print("CONFUSION MATRIX")
        print(
            confusion_matrix(
                y_test,
                predictions
            )
        )

        detection_accuracy.objects.create(
            names=name,
            ratio=accuracy
        )

    # SAVE PREDICTIONS
    predicts = 'predicts.csv'

    df.to_csv(
        predicts,
        index=False
    )

    obj = detection_accuracy.objects.all()

    return render(
        request,
        'SProvider/Train_Test_DataSets.html',
        {'objs': obj}
    )