from datetime import datetime as dt
import random
import string
def generate_token():
    return dt.now().strftime("%S%M%H%m%d%Y") +\
        "".join(random.choice(string.ascii_letters) for i in range(114))