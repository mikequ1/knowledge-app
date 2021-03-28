from profanity_check import predict, predict_prob #this is a library that does pretty much what we were going to code

def checkstr(str):
    return predict([str])

def probstr(str):
    return predict_prob([str])

print(checkstr('Firebase Authentication does automatically remember authentication state, so the user will still be authenticated when the app is restarted.'))
print(probstr('Firebase Authentication does automatically remember authentication state, so the user will still be authenticated when the app is restarted. fuck.'))

#original code below:
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.calibration import CalibratedClassifierCV
from sklearn.svm import LinearSVC

data = pd.read_csv('data.csv')
strings = data['text'].astype(str)
offensive = data['is_offensive'].astype(bool)
#compile info from the data set

vector = CountVectorizer()
model = LinearSVC(class_weight="balanced") #create a model
tofit = CalibratedClassifierCV(base_estimator = model)
tofit.fit(vector.fit_transform(strings, offensive), offensive)
#basically uses BOW (which is count vectorizer) algorithm to relate word frequency to whether that word is offensive
#when we combine that with an entire string containing other words, we get a relationship that states whether its offensive or not

#couldn't run it with flask : (
#see /pythonjslink and app.py
