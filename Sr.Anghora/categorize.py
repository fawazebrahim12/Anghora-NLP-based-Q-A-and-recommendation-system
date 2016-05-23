import alchemy

def categorize(query):
    ptr = alchemy.AlchemyAPI('ad1e1029ca5d1eaf1f7abf84e751e7ea021bd8a7')
    try:
        json_obj =  ptr.taxonomy('text',query)
        li = []
        for i in range(0,int(len(json_obj['taxonomy']))):
            k = json_obj['taxonomy'][i]['label'].split('/')
            k = list(filter(None, k))
            li.append(k[0])
        
        top_li =[]
        [top_li.append(item) for item in li if item not in top_li]
        if top_li:
            return top_li[0]
        else:
            return None
    except:
       return None
