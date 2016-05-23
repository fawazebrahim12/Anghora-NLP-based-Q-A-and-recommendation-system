from flask import Flask, request
import re, time, json, csv, os, random
from collections import Counter
#from multiprocessing import Process
import wolf, Bing, ai, knowledgegraph, Places, DistMatrix, categorize, Pearson_collab

from datetime import timedelta
from flask import make_response, request, current_app
from functools import update_wrapper

directory = "users/"
def crossdomain(origin=None, methods=None, headers=None,
                max_age=21600, attach_to_all=True,
                automatic_options=True):
    if methods is not None:
        methods = ', '.join(sorted(x.upper() for x in methods))
    if headers is not None and not isinstance(headers, str):
        headers = ', '.join(x.upper() for x in headers)
    if not isinstance(origin, str):
        origin = ', '.join(origin)
    if isinstance(max_age, timedelta):
        max_age = max_age.total_seconds()

    def get_methods():
        if methods is not None:
            return methods

        options_resp = current_app.make_default_options_response()
        return options_resp.headers['allow']

    def decorator(f):
        def wrapped_function(*args, **kwargs):
            if automatic_options and request.method == 'OPTIONS':
                resp = current_app.make_default_options_response()
            else:
                resp = make_response(f(*args, **kwargs))
            if not attach_to_all and request.method != 'OPTIONS':
                return resp

            h = resp.headers
            h['Access-Control-Allow-Origin'] = origin
            h['Access-Control-Allow-Methods'] = get_methods()
            h['Access-Control-Max-Age'] = str(max_age)
            h['Access-Control-Allow-Credentials'] = 'true'
            h['Access-Control-Allow-Headers'] = \
                "Origin, X-Requested-With, Content-Type, Accept, Authorization"
            if headers is not None:
                h['Access-Control-Allow-Headers'] = headers
            return resp

        f.provide_automatic_options = False
        return update_wrapper(wrapped_function, f)
    return decorator

app = Flask(__name__)

def recDict(id):
    dictionary = {}
    for root,dirs,files in os.walk(directory):
        for file in files:
            if file.endswith(".csv"):
                with open(directory + file,'r') as myfile:
                    li = []
                    r = csv.reader(myfile)
                    for row in r:
                        li.append(row[1])
                name = os.path.splitext(os.path.basename(directory + file))[0]
                di = dict(Counter(li))
                t = sorted(di.items(), key=lambda x:-x[1])[:8]
                di = {x:y for x,y in t}
            dictionary[name] = di
        category = Pearson_collab.pearson_collab(dictionary,id)
        f = open(directory + "data.json")
        d = f.read()
        f.close()
        dataset = json.loads(d)
        di = random.sample(set(dataset[category]), 8)
    return di
    
def distance(query):
        
        distMatrix = {}
        query = re.sub('\W+',' ', query)
        tokens = query.split()
        distancekeys = ['what','is','d','the','dist','distance','btw','between','time','taken','take','travel','reach','how','much','does','it']
        tokens = [w for w in tokens if w not in distancekeys]
        key = ['to','from','and','nd']
        try:
                while tokens[0] in key:
                        tokens.pop(0)
        except:
                pass
        query = ' '.join(tokens)
        if 'from' in tokens:
                li = query.split(" from ")
                #print (li[::-1])
        elif 'and' in tokens:
                li = query.split(" and ")
                #print (li)
        elif 'nd' in tokens:
                li = query.split(" nd ")
                #print (li)
        else:
                li = query.split(" to ")
                #print (li)
        try:
                distMatrix = DistMatrix.distMatrix(li[0],li[1])
        except:
                pass
        if distMatrix:
                return distMatrix
        else:
                return None
            
@app.route('/')
@crossdomain(origin='*')
def data():
    query = request.args.get('q')
    id = request.args.get('id')
    resp ={}
    
    #alchemyapi
    resp['alchemy_result'] = categorize.categorize(query)
    if(int(id)>0):
        if(resp['alchemy_result']):
            mylist = [query,resp['alchemy_result']]
            with open(directory + id +'.csv','a') as myfile:
                wr = csv.writer(myfile,lineterminator='\n')
                wr.writerow(mylist)
        resp['recommend'] = recDict(id)
    start = time.time()
    
    correction = Bing.spellingsuggestions(query)
    if correction:
        resp['correction'] = correction
        query = correction
    else:
            resp['correction'] = None
    
    '''
    p1 = Process(target = bing(query))
    p1.start()
    p2 = Process(target = wolf.wolfaramalpha(query))
    p2.start()
    #p1.join()
    #p2.join()
    '''
    
    #wolframAlpha
    #resp['wolf_result'] = wolf.wolfaramalpha(query)
    
    #bing
    #bing(query)
    imagekeys = ["image" , "img" , "photo" , "wallpaper"]
    videokeys = ["video" , "youtube" , "dailymotion"]
    newskeys = ["news" , "updates"]
    tokens = query.split()
    
    image_result = video_result = news_result = None
        
    if any(x in query for x in imagekeys):
        image_result = Bing.image(query,20)

    elif any(x in query for x in videokeys):
        video_result = Bing.video(query,10)

    elif any(x in query for x in newskeys):
        news_result = Bing.news(query,15)
            
    resp['web_result'] = Bing.web(query)
    resp['rs_result'] = Bing.relatedsearch(query)
    #resp['image_result'] = image_result
    #resp['video_result'] = video_result
    #resp['news_result'] = news_result

    #ai
    resp['ai_result'] = ai.ai(query)
    
    #DistMatrix
    #resp['distMatrix'] = distance(query)
    
    #knowledgegraph
    resp['kg_result'] = knowledgegraph.knowledgegraph(query)

    #Places
    #resp['places_result'] = Places.Places(query)

    #print (resp)
    json_object = json.dumps(resp)
    return json_object

    #print(time.time()-start)

if __name__ == '__main__':
    app.run(threaded=True)


