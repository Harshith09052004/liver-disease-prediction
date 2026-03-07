from django.shortcuts import render, redirect
from django.conf import settings
from liver_disease_prediction.Remote_User.models import ClientRegister_Model, disease_prediction

import pandas as pd
import numpy as np
import os

from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer


# ---------------- LOGIN ----------------
def login(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        user = ClientRegister_Model.objects.filter(
            username=username,
            password=password
        ).first()

        if user:
            request.session["userid"] = user.id
            return redirect('ViewYourProfile')

        else:
            return render(
                request,
                'htmls/RUser/login.html',
                {"error": "Invalid username or password"}
            )

    return render(request, 'htmls/RUser/login.html')
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

        return redirect('login')

    return render(request, 'htmls/RUser/Register1.html')


# ---------------- PROFILE ----------------
def ViewYourProfile(request):

    userid = request.session.get('userid')

    if not userid:
        return redirect('login')

    user = ClientRegister_Model.objects.get(id=userid)

    return render(request, 'htmls/RUser/ViewYourProfile.html', {'object': user})


# ---------------- PREDICTION ----------------
def Predict_Liver_Disease_Status(request):

    if request.method == "POST":

        try:

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

            csv_path = os.path.join(settings.BASE_DIR, "liver_patient.csv")
            df = pd.read_csv(csv_path)

            features = [
                'Age',
                'Total_Bilirubin',
                'Direct_Bilirubin',
                'Alkaline_Phosphotase',
                'Alamine_Aminotransferase',
                'Aspartate_Aminotransferase',
                'Total_Protiens',
                'Albumin',
                'Albumin_and_Globulin_Ratio'
            ]

            X = df[features]
            y = df['Dataset']

            y = y.apply(lambda x: 1 if x == 1 else 0)

            imputer = SimpleImputer(strategy='mean')
            X = imputer.fit_transform(X)

            scaler = StandardScaler()
            X = scaler.fit_transform(X)

            model = LogisticRegression(max_iter=1000)
            model.fit(X, y)

            input_imputed = imputer.transform([input_data])
            input_scaled = scaler.transform(input_imputed)

            prediction = model.predict(input_scaled)[0]

            if prediction == 1:
                result = "Found Liver Disease"
            else:
                result = "No Liver Disease"

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

            return render(request, 'htmls/RUser/Predict_Liver_Disease_Status.html', {'objs': result})

        except Exception as e:

            return render(request, 'htmls/RUser/Predict_Liver_Disease_Status.html', {"error": str(e)})

    return render(request, 'htmls/RUser/Predict_Liver_Disease_Status.html')
