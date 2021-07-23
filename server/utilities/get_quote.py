import requests as req
import random
options = ["general", "beauty","best","motivational","music","patience","peace"]

def get_quote():
    res = req.get(f"https://goquotes-api.herokuapp.com/api/v1/random?count=1&type={random.choice(options)}")
    quote = res.json()["quotes"][0]["text"]
    if(len(quote)>260):
        return get_quote()
    else:
        return quote
