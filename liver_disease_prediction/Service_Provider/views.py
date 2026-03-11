from django.shortcuts import render
from django.conf import settings

from liver_disease_prediction.Remote_User.models import ClientRegister_Model, disease_prediction

import pandas as pd
import os


def serviceproviderlogin(request):

    if request.method == "POST":

        username = request.POST.get('username')
        password = request.POST.get('password')

        if username == "ServiceProvider" and password == "ServiceProvider":

            request.session['sp'] = True
            return render(request, 'htmls/SProvider/serviceproviderhome.html')

        return render(request,
                      'htmls/SProvider/serviceproviderlogin.html',
                      {"error": "Invalid Login"})

    return render(request,
                  'htmls/SProvider/serviceproviderlogin.html')


def View_Remote_Users(request):

    users = ClientRegister_Model.objects.all()

    return render(request,
                  'htmls/SProvider/View_Remote_Users.html',
                  {"objects": users})


def View_Liver_Disease_Status(request):

    objs = disease_prediction.objects.all()

    return render(request,
                  'htmls/SProvider/View_Liver_Disease_Status.html',
                  {"objs": objs})


def Train_Test_DataSets(request):

    csv_path = os.path.join(settings.BASE_DIR, "liver_patient.csv")

    if os.path.exists(csv_path):

        df = pd.read_csv(csv_path)
        data = df.head(100).to_html()

    else:

        data = "Dataset file not found."

    return render(request,
                  'htmls/SProvider/Train_Test_DataSets.html',
                  {"data": data})


def Find_Liver_Disease_Ratio(request):

    csv_path = os.path.join(settings.BASE_DIR, "liver_patient.csv")

    if os.path.exists(csv_path):

        df = pd.read_csv(csv_path)

        disease = len(df[df['Dataset'] == 1])
        nodisease = len(df[df['Dataset'] == 2])

    else:

        disease = 0
        nodisease = 0

    return render(request,
                  'htmls/SProvider/Find_Liver_Disease_Ratio.html',
                  {"disease": disease, "nodisease": nodisease})
