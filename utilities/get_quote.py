import requests as req
import random
options = ["faith", "famous-quotes", "friendship", "future", "happiness", "inspirational", "life", "love", "proverb", "success", "wisdom"]

def get_quote(i):
    if(i>=0):
        i-=1
        res = req.get(f"https://api.quotable.io/random?tags={random.choice(options)}")
        quote = res.json()["content"]
        if(len(quote)>260):
            return get_quote()
        else:
            return quote
    else:
        return ""
