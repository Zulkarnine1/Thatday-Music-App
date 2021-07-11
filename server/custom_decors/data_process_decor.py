from functools import wraps
from ..main import  current_user

def process_user(f):
    @wraps(f)
    def decor(*args,**kwargs):
        if current_user:
            user_data = {
                "name":current_user.name,
                "img":current_user.img,
                "username":current_user.username,
            }
        return user_data
    return decor()