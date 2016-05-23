from urllib.parse import quote
import requests

API_KEY = 'c+YY0LKcxPHuYUg6aHFGI/6sZs0Sl41/6/gxFuXc73U'

def web(query,top=10):
    query=query.lstrip()
    query=quote(query)
    result=requests.get('https://api.datamarket.azure.com/Data.ashx/Bing/Search/Web?Query=%27' + query + '%27&$format=json&$top=' + str(top), auth=(API_KEY, API_KEY)).json()
    resp = []
    for i in range(len(result['d']['results'])):
        Title = result['d']['results'][i]['Title']
        Description = result['d']['results'][i]['Description']
        Url = result['d']['results'][i]['Url']
        res ={}
        res['Title']=Title
        res['Description']=Description
        res['Url']=Url

        resp.append(res)
    
    if resp:
        return resp
    else:
        return None
    

def image(query,top=1):
    query=query.lstrip()
    query=quote(query)
    result=requests.get("https://api.datamarket.azure.com/Data.ashx/Bing/Search/Image?Query=%27" + query + "%27&$format=json&$top=" + str(top), auth=(API_KEY, API_KEY)).json()
    resp = []
    for i in range(len(result['d']['results'])):
        Title = result['d']['results'][i]['Title']
        MediaUrl = result['d']['results'][i]['MediaUrl']
        Url = result['d']['results'][i]['SourceUrl']
        res = {}
        res['Title'] = Title
        res['MediaUrl'] = MediaUrl
        res['Url'] = Url

        resp.append(res)
    
    if resp:
        return resp
    else:
        return None

def news(query,top=5):
    query=query.lstrip()
    query=quote(query)
    result=requests.get('https://api.datamarket.azure.com/Data.ashx/Bing/Search/News?Query=%27' + query + '%27&$format=json&$top=' + str(top), auth=(API_KEY, API_KEY)).json()
    resp = []
    for i in range(len(result['d']['results'])):
        Title = result['d']['results'][i]['Title']
        Source = result['d']['results'][i]['Source']
        Date = result['d']['results'][i]['Date']
        Description = result['d']['results'][i]['Description']
        Url = result['d']['results'][i]['Url']
        
        res = {}
        res['Title'] = Title
        res['Source'] = Source
        res['Date'] = Date
        res['Description'] = Description
        res['Url'] = Url

        resp.append(res)
    
    if resp:
        return resp
    else:
        return None
    
def video(query,top=1):
    query=query.lstrip()
    query=quote(query)
    result=requests.get("https://api.datamarket.azure.com/Data.ashx/Bing/Search/Video?Query=%27" + query + "%27&$format=json&$top=" + str(top), auth=(API_KEY, API_KEY)).json()
    resp = []
    for i in range(len(result['d']['results'])):
        Title = result['d']['results'][i]['Title']
        MediaUrl = result['d']['results'][i]['MediaUrl']
        Thumbnail = result['d']['results'][i]['Thumbnail']['MediaUrl']
        RunTime = result['d']['results'][i]['RunTime']
        totalsecs = int(RunTime) / 1000
        mins = int(totalsecs / 60)
        secs = int(totalsecs % 60)
        
        res = {}
        res['Title'] = Title
        res['MediaUrl'] = MediaUrl
        res['Thumbnail'] = Thumbnail
        res['min'] = mins
        res['sec'] = secs

        resp.append(res)
    
    if resp:
        return resp
    else:
        return None

def relatedsearch(query,top=5):
    query=query.lstrip()
    query=quote(query)
    result=requests.get('https://api.datamarket.azure.com/Data.ashx/Bing/Search/RelatedSearch?Query=%27' + query + '%27&$format=json&$top=' + str(top), auth=(API_KEY, API_KEY)).json()
    
    resp = []
    for i in range(len(result['d']['results'])):
        Title = result['d']['results'][i]['Title']
        BingUrl = result['d']['results'][i]['BingUrl']
        
        res = {}
        res['Title'] = Title
        res['BingUrl'] = BingUrl

        resp.append(res)
    
    if resp:
        return resp
    else:
        return None

def spellingsuggestions(query):
    query=query.lstrip()
    query=quote(query)
    result=requests.get('https://api.datamarket.azure.com/Data.ashx/Bing/Search/SpellingSuggestions?Query=%27' + query + '%27&$format=json&$top=1', auth=(API_KEY, API_KEY)).json()
    try:
        Title = result['d']['results'][0]['Value']
        return Title
    except:
        return

