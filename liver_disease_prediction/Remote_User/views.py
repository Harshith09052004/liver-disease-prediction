from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect
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
from sklearn.ensemble import RandomForestClassifier, VotingClassifier
from sklearn.neighbors import KNeighborsClassifier

from Remote_User.models import (
    ClientRegister_Model,
    disease_prediction,
    detection_ratio,
    detection_accuracy
)


# LOGIN
def login(request):

    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            enter = ClientRegister_Model.objects.get(
                username=username,
                password=password
            )

            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')

        except:
            pass

    return render(request, 'RUser/login.html')


# REGISTER
def Register1(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')

        ClientRegister_Model.objects.create(
            username=username,
            email=email,
            password=password,
            phoneno=phoneno,
            country=country,
            state=state,
            city=city
        )

        return render(request, 'RUser/Register1.html')

    else:

        return render(request, 'RUser/Register1.html')


# VIEW PROFILE
def ViewYourProfile(request):

    userid = request.session['userid']

    obj = ClientRegister_Model.objects.get(
        id=userid
    )

    return render(
        request,
        'RUser/ViewYourProfile.html',
        {'object': obj}
    )


# PREDICT LIVER DISEASE
def Predict_Liver_Disease_Status(request):

    if request.method == "POST":

        Pid = request.POST.get('Pid')

        Age = float(request.POST.get('Age'))

        Gender = request.POST.get('Gender')

        Total_Bilirubin = float(
            request.POST.get('Total_Bilirubin')
        )

        Direct_Bilirubin = float(
            request.POST.get('Direct_Bilirubin')
        )

        Alkaline_Phosphotase = float(
            request.POST.get('Alkaline_Phosphotase')
        )

        Alamine_Aminotransferase = float(
            request.POST.get('Alamine_Aminotransferase')
        )

        Aspartate_Aminotransferase = float(
            request.POST.get('Aspartate_Aminotransferase')
        )

        Total_Protiens = float(
            request.POST.get('Total_Protiens')
        )

        Albumin = float(
            request.POST.get('Albumin')
        )

        Albumin_and_Globulin_Ratio = float(
            request.POST.get('Albumin_and_Globulin_Ratio')
        )

        # LOAD DATASET
        df = pd.read_csv('liver_patient.csv')

        # REMOVE NULL VALUES
        df.dropna(inplace=True)

        # CONVERT GENDER
        df['Gender'] = df['Gender'].map({
            'Male': 1,
            'Female': 0
        })

        # TARGET VARIABLE
        def apply_results(results):

            if results <= 1.2 and results >= 0.1:
                return 0

            else:
                return 1

        df['Results'] = df['Direct_Bilirubin'].apply(
            apply_results
        )

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

        # TRAIN TEST SPLIT
        X_train, X_test, y_train, y_test = train_test_split(
            X,
            y,
            test_size=0.20,
            random_state=42
        )

        # MODELS
        models = []

        # NAIVE BAYES
        nb = GaussianNB()
        nb.fit(X_train, y_train)
        models.append(('naive_bayes', nb))

        # SVM
        svm_model = SVC(probability=True)
        svm_model.fit(X_train, y_train)
        models.append(('svm', svm_model))

        # LOGISTIC REGRESSION
        lr = LogisticRegression(max_iter=1000)
        lr.fit(X_train, y_train)
        models.append(('logistic', lr))

        # DECISION TREE
        dt = DecisionTreeClassifier()
        dt.fit(X_train, y_train)
        models.append(('decision_tree', dt))

        # RANDOM FOREST
        rf = RandomForestClassifier()
        rf.fit(X_train, y_train)
        models.append(('random_forest', rf))

        # KNN
        knn = KNeighborsClassifier()
        knn.fit(X_train, y_train)
        models.append(('knn', knn))

        # VOTING CLASSIFIER
        classifier = VotingClassifier(estimators=models)

        classifier.fit(X_train, y_train)

        # USER INPUT
        gender_value = 1 if Gender == "Male" else 0

        user_data = [[
            Age,
            gender_value,
            Total_Bilirubin,
            Direct_Bilirubin,
            Alkaline_Phosphotase,
            Alamine_Aminotransferase,
            Aspartate_Aminotransferase,
            Total_Protiens,
            Albumin,
            Albumin_and_Globulin_Ratio
        ]]

        # SCALE USER INPUT
        user_data = scaler.transform(user_data)

        # PREDICT
        prediction = classifier.predict(user_data)[0]

        # RESULT
        if prediction == 0:

            val = 'No Liver Disease'

        else:

            val = 'Found Liver Disease'

        print(val)

        # SAVE RESULT
        disease_prediction.objects.create(
            Pid=Pid,
            Age=Age,
            Gender=Gender,
            Total_Bilirubin=Total_Bilirubin,
            Direct_Bilirubin=Direct_Bilirubin,
            Alkaline_Phosphotase=Alkaline_Phosphotase,
            Alamine_Aminotransferase=Alamine_Aminotransferase,
            Aspartate_Aminotransferase=Aspartate_Aminotransferase,
            Total_Protiens=Total_Protiens,
            Albumin=Albumin,
            Albumin_and_Globulin_Ratio=Albumin_and_Globulin_Ratio,
            prediction=val
        )

        return render(
            request,
            'RUser/Predict_Liver_Disease_Status.html',
            {'objs': val}
        )

    return render(
        request,
        'RUser/Predict_Liver_Disease_Status.html'
    )