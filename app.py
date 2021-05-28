from typing import final
from flask import Flask, render_template, flash, request
import joblib as joblib
import os
import hashlib
import requests
import json
import base64

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))
app.config['SECRET_KEY'] = 'abc123@567$#'

def callEnzoicAPI(password):
    apiKey = ''
    secretKey = ''
    authorizationParameter = apiKey+":"+secretKey
    authorizationParameter = authorizationParameter.encode('ascii')
    authorizationParameter = (base64.b64encode(authorizationParameter)).decode('ascii')
    authorizationParameter = "basic "+str(authorizationParameter)
    print(authorizationParameter)
    password = password.encode('utf-8')
    sha1HashTemp = hashlib.sha1(password)
    sha1Hash = str(sha1HashTemp.hexdigest())
    sha256HashTemp = hashlib.sha256(password)
    sha256Hash = str(sha256HashTemp.hexdigest())
    md5HashTemp = hashlib.md5(password)
    md5Hash = str(md5HashTemp.hexdigest())
    rawData = {'partialSHA1':sha1Hash, 'partialSHA256':sha256Hash, 'partialMD5':md5Hash}
    url = 'https://api.enzoic.com/passwords'
    #authorization parameter is basic BASE64(APIKEY:SECRETKEY)
    response = requests.post(url, data = json.dumps(rawData),headers={'content-type':'application/json',
    'authorization':authorizationParameter})
    if(response.status_code == 404):
        print("Not found")
        return False,0
    finalResponse = response.conten.decode('ascii')
    return finalResponse["candidates"][0]["revealedInExposure"], finalResponse["candidates"][0]["exposureCount"]


@app.route('/')
def homepage():
    hi = callEnzoicAPI("EarthingIsNoob123")
    print(hi[0], hi[1])
    return render_template('index.html')


@app.route('/main/', methods=['GET', 'POST'])
def mainpage():
    if request.method == "POST":
        enteredPassword = request.form['password']
    else:
        return render_template('index.html')

    # Load the algorithm models
    DecisionTree_Model = joblib.load('DecisionTree_Model.joblib')
    print("Decision Tree Loaded")
    LogisticRegression_Model = joblib.load('LogisticRegression_Model.joblib')
    NaiveBayes_Model = joblib.load('NaiveBayes_Model.joblib')
    NeuralNetwork_Model = joblib.load('NeuralNetwork_Model.joblib')
    
    Password = [enteredPassword]

    # Predict the strength
    DecisionTree_Test = DecisionTree_Model.predict(Password)
    LogisticRegression_Test = LogisticRegression_Model.predict(Password)
    NaiveBayes_Test = NaiveBayes_Model.predict(Password)
    NeuralNetwork_Test = NeuralNetwork_Model.predict(Password)
    apiResult = callEnzoicAPI(Password)

    return render_template("main.html", DecisionTree=DecisionTree_Test,
                                        LogReg=LogisticRegression_Test, 
                                        NaiveBayes=NaiveBayes_Test,
                                        NeuralNetwork=NeuralNetwork_Test
                                        )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
