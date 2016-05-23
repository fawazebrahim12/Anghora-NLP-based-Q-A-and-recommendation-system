import googlemaps
api_key ='AIzaSyBf0BCaCQL0BO0nOtGo6NQe0WGTFPJMNMY'
gmaps = googlemaps.Client(key = api_key)
def distMatrix(origin,destination):
    resp ={}
    try:
        res = gmaps.distance_matrix(origin,destination)
        origin = res['origin_addresses'][0]
        destination = res['destination_addresses'][0]
        duration = res['rows'][0]['elements'][0]['duration']['text']
        distance = res['rows'][0]['elements'][0]['distance']['text']
        
        resp['origin'] = origin
        resp['destination'] = destination
        resp['duration'] = duration
        resp['distance'] = distance
    except:
        pass
    return resp
