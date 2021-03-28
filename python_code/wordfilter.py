from profanity_check import predict, predict_prob

def checkstr(str):
    return predict([str])

def probstr(str):
    return predict_prob([str])

print(checkstr('Firebase Authentication does automatically remember authentication state, so the user will still be authenticated when the app is restarted.'))
print(probstr('Firebase Authentication does automatically remember authentication state, so the user will still be authenticated when the app is restarted. fuck.'))

#pip install alt-profanity-check