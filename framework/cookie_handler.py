from hashlib import sha256

SECRET = "LKJHASDLKIUHnN872134n9QERFNZCVnwencvuplmkmM95m2M+jhasdfhaskdjfh+21238hHelqCXBV523g12312t6540494875"

def sign_cookie(value):
    string_value = str(value)
    signature = sha256(SECRET + string_value).hexdigest()
    return signature + "|" + string_value
def check_cookie(value):
    signature = value[:value.find('|')]
    declared_value = value[value.find('|') + 1:]

    if sha256(SECRET + declared_value).hexdigest() == signature:
        return declared_value
    else:
        return None