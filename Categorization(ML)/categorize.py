from textblob.classifiers import NaiveBayesClassifier
import pickle
from textblob import TextBlob
import time
stime = time.time()
print ("classifier running............")
with open('result15.csv','r') as fp:
    f = open('my_classifier.pickle', 'wb')
    pickle.dump(NaiveBayesClassifier(fp,format='csv'), f)
    f.close()
print(time.time() - stime)
