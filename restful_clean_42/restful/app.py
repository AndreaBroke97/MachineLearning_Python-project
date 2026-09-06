from flask import Flask, request, render_template, redirect, url_for
import pandas as pd
import numpy as np
from joblib import load

app = Flask(__name__)

try:
    model = load("modello_mutuo.joblib")
except FileNotFoundError:
    model = None
    print("Errore: file modello_mutuo.joblib non trovato")
except Exception as error:
    model = None
    print("Errore nel caricamento del modello:", error)

def predici_mutuo(dati_cliente):
    tabella = pd.DataFrame([dati_cliente])
    predizione = model.predict(tabella)[0]
    probabilita = model.predict_proba(tabella)[0, 1]
    return {
        "esito": "APPROVATO" if predizione == 1 else "RIFIUTATO",
        "approvato": predizione == 1,
        "probabilita": float(np.round(probabilita, 3))
    }

def leggi_dati_form(form):
    dati = {
        "Gender": form["Gender"],
        "Married": form["Married"],
        "Education": form["Education"],
        "Self_Employed": form["Self_Employed"],
        "Property_Area": form["Property_Area"],
        "Dependents": int(form["Dependents"]),
        "ApplicantIncome": int(form["ApplicantIncome"]),
        "CoapplicantIncome": int(form["CoapplicantIncome"]),
        "LoanAmount": int(form["LoanAmount"]),
        "Loan_Amount_Term": int(form["Loan_Amount_Term"]),
        "Credit_History": float(form["Credit_History"]),
    }
    return dati

@app.route('/')
def index():
    return render_template('index.html')

@app.route("/predict", methods = ["POST"])
def predict():
    if model is None:
        return render_template("index.html", errore = "Modello non disponibile")

    try:
        dati_cliente = leggi_dati_form(request.form)
    except (KeyError, ValueError):
        return render_template("index.html", errore = "Dati mancanti o non validi")

    try:
        risultato = predici_mutuo(dati_cliente)
    except Exception:
        return render_template("index.html", errore = "Errore durante la previsione")

    if risultato["approvato"]:
        return redirect(url_for("success"))
    else:
        return redirect(url_for("fail"))
    
@app.route("/success")
def success():
    return render_template("success.html")

@app.route("/fail")
def fail():
    return render_template("fail.html")

if __name__ == '__main__':
	app.run(debug=True) 