# ANN

# Import the necessary Libraries
import pandas as pd
import time

# For text feature extraction
from sklearn.feature_extraction.text import TfidfVectorizer

# For creating a pipeline
from sklearn.pipeline import Pipeline

# Classifier Model (MultiLayer Perceptron)
from sklearn.neural_network import MLPClassifier

# To save the trained model on local storage
import joblib

start_time = time.time()
# Read the File
data = pd.read_csv('data.csv')

# Features which are passwords
features = data.values[:, 1].astype('str')

# Labels which are strength of password
labels = data.values[:, -1].astype('int')

# Splitting the dataset into the training and test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test=train_test_split(features,labels,test_size=0.25,random_state=0)

# Sequentially apply a list of transforms and a final estimator
classifier_model = Pipeline([
                ('tfidf', TfidfVectorizer(analyzer='char')),
                ('mlpClassifier', MLPClassifier(solver='adam', 
                                                alpha=1e-5, 
                                                max_iter=400,
                                                activation='logistic')),
])

# Fit the Model
classifier_model.fit(X_train, y_train)

y_pred = classifier_model.predict(X_test)

from sklearn.metrics import confusion_matrix, classification_report
cm=confusion_matrix(y_test,y_pred)
print(classification_report(y_test, y_pred, digits=4))
print("Confusion Matrix: \n", cm)
accuracy = (cm[0][0]+cm[1][1]+cm[2][2])/(cm[0][0]+cm[0][1]+cm[0][2]+cm[1][0]+cm[1][1]+cm[1][2]+cm[2][0]+cm[2][1]+cm[2][2])
print('Training Accuracy: ',classifier_model.score(features, labels))
print("Testing Accuracy = ", accuracy)
print("Time Taken to train the model = %s seconds" % round((time.time() - start_time),2))
# Save model
joblib.dump(classifier_model, 'NeuralNetwork_Model.joblib')