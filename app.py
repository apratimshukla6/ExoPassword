from flask import Flask, render_template, flash, request
import joblib as joblib
import os

app = Flask(__name__)
port = int(os.environ.get('PORT', 5000))
app.config['SECRET_KEY'] = 'abc123@567$#'

@app.route('/')
def homepage():
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
    

    return render_template("main.html", DecisionTree=DecisionTree_Test,
                                        LogReg=LogisticRegression_Test, 
                                        NaiveBayes=NaiveBayes_Test,
                                        NeuralNetwork=NeuralNetwork_Test
                                        )

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=port)
