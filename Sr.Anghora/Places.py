import googlemaps
import prettyTime
import sys

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

api_key = 'AIzaSyBf0BCaCQL0BO0nOtGo6NQe0WGTFPJMNMY' #'AIzaSyA725qQgWsr-EkScxcya3l8qGqZXWCxFsg'
gmaps = googlemaps.Client(key = api_key)

def Places(query):
    places = gmaps.places(query)
    result = places['results']
    resp = []
    for i in result:
        data = {}

        place_id = i['place_id']
        placeDetail = gmaps.place(place_id)
        
        name = i['name']
        data['name'] = name
        
        try:
            rating = i['rating']
            data['rating'] = rating
            
            total_reviews = placeDetail['result']['user_ratings_total']
            data['total_reviews'] = total_reviews
        except:
            pass

        type = i['types'][0]
        if type not in ['point_of_interest','establishment']:
            data['type'] = type

        address = i['formatted_address']
        data['address'] = address
        
        try:
            phone_no = placeDetail['result']['international_phone_number']
            data['phone_no'] = phone_no
            
        except:
            pass
        try:
            uri = placeDetail['result']['url']
            data['uri'] = uri
            
        except:
            pass
        try:
            website = placeDetail['result']['website']
            data['website'] = website
            
        except:
            pass
        
        try:
            open_now = placeDetail['result']['opening_hours']['open_now']
            data['open_now'] = open_now
            
        except:
            pass
        try:
            hours = placeDetail['result']['opening_hours']['weekday_text']
            data['Hours'] = hours
            
        except:
            pass

        try:
            reviews = placeDetail['result']['reviews']
            

            sdata = []
            for j in reviews:
                rev = {}
                author_name = j['author_name']
                rev['author_name'] = author_name
                
                try:
                    gplus = j['author_url']
                    rev['gplus'] = gplus
                    
                except:
                    pass
                
                rating = j['rating']
                rev['rating'] = rating
               
                
                text = j['text'].translate(non_bmp_map)
                rev['text'] = text
               

                time = j['time']
                postTime = prettyTime.pretty_date(time)
                rev['posttime'] = postTime
                
                try:
                    dp = j['profile_photo_url']
                    rev['dp'] = dp
                    
                except:
                    pass

                #append rev to data
                sdata.append(rev)

            data['rev'] = sdata

        except:
            pass
                
        try:   
            photos = placeDetail['result']['photos']
            photo_uri = []
            for j in photos:
                photoreference = j['photo_reference']
                max_width = str(j['width'])
                uri = 'https://maps.googleapis.com/maps/api/place/photo?photoreference=' + photoreference + '&maxwidth=' + max_width + '&key=' + api_key
                photo_uri.append(uri)
                
                
            data['photo_uri'] = photo_uri

        except:
            pass

        resp.append(data)

    if resp:
        return resp
    else:
        return None
