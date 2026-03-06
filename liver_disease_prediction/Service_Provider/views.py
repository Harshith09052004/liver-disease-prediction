from django.shortcuts import render
from django.conf import settings

from liver_disease_prediction.Service_Provider.models import *
from liver_disease_prediction.Remote_User.models import ClientRegister_Model, disease_prediction

import pandas as pd
import os


# ---------------- SERVICE PROVIDER LOGIN ----------------
def serviceproviderlogin(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "ServiceProvider" and password == "ServiceProvider":

            request.session['sp'] = True
            return render(request, 'SProvider/serviceproviderhome.html')

        else:
            return render(
                request,
                'SProvider/serviceproviderlogin.html',
                {"error": "Invalid Login"}
            )

    return render(request, 'SProvider/serviceproviderlogin.html')


# ---------------- VIEW USERS ----------------
def View_Remote_Users(request):

    users = ClientRegister_Model.objects.all()

    return render(
        request,
        'SProvider/View_Remote_Users.html',
        {"objects": users}
    )


# ---------------- VIEW PREDICTIONS ----------------
def View_Liver_Disease_Status(request):

    objs = disease_prediction.objects.all()

    return render(
        request,
        'SProvider/View_Liver_Disease_Status.html',
        {"objs": objs}
    )


# ---------------- TRAIN TEST DATA ----------------
def Train_Test_DataSets(request):

    csv_path = os.path.join(settings.BASE_DIR, "liver_patient.csv")
    df = pd.read_csv(csv_path)

    return render(
        request,
        'SProvider/Train_Test_DataSets.html',
        {"data": df.head(100).to_html()}
    )


# ---------------- DATASET RATIO ----------------
def Find_Liver_Disease_Ratio(request):

    csv_path = os.path.join(settings.BASE_DIR, "liver_patient.csv")
    df = pd.read_csv(csv_path)

    disease = len(df[df['Dataset'] == 1])
    nodisease = len(df[df['Dataset'] == 2])

    return render(
        request,
        'SProvider/Find_Liver_Disease_Ratio.html',
        {"disease": disease, "nodisease": nodisease}
    )


# ---------------- DOWNLOAD DATASET ----------------
def Download_Trained_DataSets(request):

    csv_path = os.path.join(settings.BASE_DIR, "liver_patient.csv")
    df = pd.read_csv(csv_path)

    return render(
        request,
        'SProvider/Download_Trained_DataSets.html',
        {"data": df.to_html()}
    )
