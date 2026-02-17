from django.shortcuts import render, redirect
from Remote_User.models import ClientRegister_Model, disease_prediction

import pandas as pd
import numpy as np

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


# ---------------- LOGIN ----------------
def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = ClientRegister_Model.objects.get(username=username, password=password)
            request.session["userid"] = user.id
            return redirect('ViewYourProfile')
        except:
            pass
    return render(request, 'RUser/login.html')


# ---------------- REGISTER ----------------
def Register1(request):
    if request.method == "POST":
        ClientRegister_Model.objects.create(
            username=request.POST.get('username'),
            email=request.POST.get('email'),
            password=request.POST.get('password'),
            phoneno=request.POST.get('phoneno'),
            country=request.POST.get('country'),
            state=request.POST.get('state'),
            city=request.POST.get('city')
        )
    return render(request, 'RUser/Register1.html')


# ---------------- PROFILE ----------------
def ViewYourProfile(request):
    user = ClientRegister_Model.objects.get(id=request.session['userid'])
    return render(request, 'RUser/ViewYourProfile.html', {'object': user})


# ---------------- PREDICTION ----------------
def Predict_Liver_Disease_Status(request):
    if request.method == "POST":

        # ---------------- USER INPUT ----------------
        input_data = [
            float(request.POST.get('Age')),
            float(request.POST.get('Total_Bilirubin')),
            float(request.POST.get('Direct_Bilirubin')),
            float(request.POST.get('Alkaline_Phosphotase')),
            float(request.POST.get('Alamine_Aminotransferase')),
            float(request.POST.get('Aspartate_Aminotransferase')),
            float(request.POST.get('Total_Protiens')),
            float(request.POST.get('Albumin')),
            float(request.POST.get('Albumin_and_Globulin_Ratio'))
        ]

        # ---------------- LOAD DATASET ----------------
        df = pd.read_csv("liver_patient.csv")

        features = [
            'Age', 'Total_Bilirubin', 'Direct_Bilirubin',
            'Alkaline_Phosphotase', 'Alamine_Aminotransferase',
            'Aspartate_Aminotransferase', 'Total_Protiens',
            'Albumin', 'Albumin_and_Globulin_Ratio'
        ]

        X = df[features]
        y = df['Dataset']   # 1 = Liver Disease, 2 = No Disease

        # Convert target to binary
        y = y.apply(lambda x: 1 if x == 1 else 0)

        # ---------------- HANDLE NaN VALUES ----------------
        imputer = SimpleImputer(strategy='mean')
        X = imputer.fit_transform(X)

        # ---------------- SCALE DATA ----------------
        scaler = StandardScaler()
        X = scaler.fit_transform(X)

        # ---------------- TRAIN MODEL ----------------
        model = LogisticRegression(max_iter=1000)
        model.fit(X, y)

        # ---------------- PREDICT ----------------
        input_imputed = imputer.transform([input_data])
        input_scaled = scaler.transform(input_imputed)

        prediction = model.predict(input_scaled)[0]

        if prediction == 1:
            result = "Found Liver Disease"
        else:
            result = "No Liver Disease"

        # ---------------- SAVE RESULT ----------------
        disease_prediction.objects.create(
            Pid=request.POST.get('Pid'),
            Age=request.POST.get('Age'),
            Gender=request.POST.get('Gender'),
            Total_Bilirubin=request.POST.get('Total_Bilirubin'),
            Direct_Bilirubin=request.POST.get('Direct_Bilirubin'),
            Alkaline_Phosphotase=request.POST.get('Alkaline_Phosphotase'),
            Alamine_Aminotransferase=request.POST.get('Alamine_Aminotransferase'),
            Aspartate_Aminotransferase=request.POST.get('Aspartate_Aminotransferase'),
            Total_Protiens=request.POST.get('Total_Protiens'),
            Albumin=request.POST.get('Albumin'),
            Albumin_and_Globulin_Ratio=request.POST.get('Albumin_and_Globulin_Ratio'),
            prediction=result
        )

        return render(request, 'RUser/Predict_Liver_Disease_Status.html', {'objs': result})

    return render(request, 'RUser/Predict_Liver_Disease_Status.html')
