from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse

from liver_disease_prediction.Service_Provider.models import *
from liver_disease_prediction.Remote_User.models import ClientRegister_Model, disease_prediction

import pandas as pd
import os


# ---------------- SERVICE PROVIDER LOGIN ----------------
from django.shortcuts import render, redirect

def serviceproviderlogin(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "ServiceProvider" and password == "ServiceProvider":
            request.session['sp'] = True
            return redirect('View_Remote_Users')

        else:
            return render(
                request,
                'htmls/SProvider/serviceproviderlogin.html',
                {"error": "Invalid Login"}
            )

    return redirect('View_Remote_Users')
# ---------------- VIEW USERS ----------------
def View_Remote_Users(request):

    users = ClientRegister_Model.objects.all()

    return render(
        request,
        'htmls/SProvider/View_Remote_Users.html',
        {"objects": users}
    )


# ---------------- VIEW PREDICTIONS ----------------
def View_Liver_Disease_Status(request):

    objs = disease_prediction.objects.all()

    return render(
        request,
        'htmls/SProvider/View_Liver_Disease_Status.html',
        {"objs": objs}
    )


# ---------------- TRAIN TEST DATA ----------------
def Train_Test_DataSets(request):

    csv_path = os.path.join(settings.BASE_DIR, "liver_patient.csv")

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        data = df.head(100).to_html()
    else:
        data = "Dataset file not found."

    return render(
        request,
        'htmls/SProvider/Train_Test_DataSets.html',
        {"data": data}
    )


# ---------------- DATASET RATIO ----------------
def Find_Liver_Disease_Ratio(request):

    csv_path = os.path.join(settings.BASE_DIR, "liver_patient.csv")

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        disease = len(df[df['Dataset'] == 1])
        nodisease = len(df[df['Dataset'] == 2])
    else:
        disease = 0
        nodisease = 0

    return render(
        request,
        'htmls/SProvider/Find_Liver_Disease_Ratio.html',
        {"disease": disease, "nodisease": nodisease}
    )


# ---------------- DOWNLOAD DATASET ----------------
def Download_Trained_DataSets(request):

    csv_path = os.path.join(settings.BASE_DIR, "liver_patient.csv")

    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        data = df.to_html()
    else:
        data = "Dataset file not found."

    return render(
        request,
        'htmls/SProvider/Download_Trained_DataSets.html',
        {"data": data}
    )


# ---------------- CHARTS ----------------
def charts(request, chart_type):
    return HttpResponse(f"Charts Page: {chart_type}")


def charts1(request, chart_type):
    return HttpResponse(f"Charts1 Page: {chart_type}")


def likeschart(request, like_chart):
    return HttpResponse(f"Likes Chart Page: {like_chart}")
