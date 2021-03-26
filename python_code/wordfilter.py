from profanity_check import predict, predict_prob

def checkstr(str):
    return predict([str])

print(checkstr('johann sucks'))
#pip install alt-profanity-check