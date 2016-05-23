import json
import urllib
import urllib.request
api_key = "AIzaSyBf0BCaCQL0BO0nOtGo6NQe0WGTFPJMNMY"
def knowledgegraph(query):
    service_url = 'https://kgsearch.googleapis.com/v1/entities:search'
    params = {
        'query': query,
        'limit': 10,
        'indent': True,
        'key': api_key,
    }
    url = service_url + '?' + urllib.parse.urlencode(params)
    response = json.loads(urllib.request.urlopen(url).read().decode('utf-8'))
    count = 0
    resp = []
    for element in response['itemListElement']:
        if(count<6):
            try:
                resultScore = element['resultScore']
            except:
                resultScore = None
            try:
                detailedDescriptionUrl = element['result']['detailedDescription']['url']
            except:
                detailedDescriptionUrl = None
                continue
            try:
                name = element['result']['name']
            except:
                name = None
                continue
            try:
                image = element['result']['image']['contentUrl']
            except:
                image = None
            try:
                description = element['result']['description']
            except:
                description = None
            try:
                detailedDescription = element['result']['detailedDescription']['articleBody']
            except:
                detailedDescription = None

            # top 6 results to be shown only
            count = count + 1
            
            data = {}
            data['resultScore'] = resultScore
            data['name'] = name
            data['image'] = image
            data['detailedDescriptionUrl'] = detailedDescriptionUrl
            data['detailedDescription'] = detailedDescription
            data['description'] = description

            #Append data to result
            resp.append(data)

    if resp:
        return resp
    else:
        return None
