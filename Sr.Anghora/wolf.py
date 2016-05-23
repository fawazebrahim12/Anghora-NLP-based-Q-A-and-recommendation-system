import wolframalpha
from collections import OrderedDict
client = wolframalpha.Client('95GTW5-U9U2YAUUA4')
def wolfaramalpha(query):
    res=client.query(query)
    resp=OrderedDict()
    for pod in res.pods:
        if pod.text is not None:
            resp[pod.title]=pod.text
    if resp:
        return resp
    else:
        return None
