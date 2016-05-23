import pickle
import time

start = time.time()
f = open('my_classifier.pickle', 'rb')
cl = pickle.load(f)
f.close()

print(cl.classify("Where to travel in bangalore ?"))
print(cl.classify("Name a golf course in Myrtle beach ."))
print(cl.classify("What body of water does the Danube River flow into ?"))
#print("Accuracy: {0}".format(cl.accuracy(test)))
print(time.time()-start)
