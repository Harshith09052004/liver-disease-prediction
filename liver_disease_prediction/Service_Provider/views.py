from django.shortcuts import render
import pickle
import os
from django.conf import settings

model_path = os.path.join(settings.BASE_DIR, "predictor", "model.pkl")

model = pickle.load(open(model_path, "rb"))

def index(request):
    return render(request, "index.html")

def predict(request):
    if request.method == "POST":
        age = float(request.POST["age"])
        tb = float(request.POST["tb"])
        db = float(request.POST["db"])
        alk = float(request.POST["alk"])
        alt = float(request.POST["alt"])
        ast = float(request.POST["ast"])
        tp = float(request.POST["tp"])
        alb = float(request.POST["alb"])
        agr = float(request.POST["agr"])

        prediction = model.predict([[age, tb, db, alk, alt, ast, tp, alb, agr]])

        if prediction[0] == 1:
            result = "Liver Disease Detected"
        else:
            result = "No Liver Disease"

        return render(request, "index.html", {"result": result})

    return render(request, "index.html")
