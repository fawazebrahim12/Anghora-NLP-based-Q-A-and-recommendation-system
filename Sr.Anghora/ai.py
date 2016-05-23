import json
import apiai
CLIENT_ACCESS_TOKEN = '99306051b475434aaf121e0c199e9dc7'
SUBSCRIPTION_KEY = '49da1b88-9c8e-43d1-9d9a-fac1514056b9'
def ai(query):
    ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN, SUBSCRIPTION_KEY)
    request = ai.text_request()
    request.lang = 'en' # optional, default value equal 'en'
    request.query = query
    response = request.getresponse()
    string = response.read().decode('utf-8')
    json_obj = json.loads(string)
    
    ans = json_obj['result']['fulfillment']['speech']
    if ans:
        return ans
    else:
        return None
