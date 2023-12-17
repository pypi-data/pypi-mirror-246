import re

def number(phone_number):   
    phone_pattern = re.compile(r'^\+998\d{9}$')
    is_valid = bool(re.match(phone_pattern, phone_number))

    if is_valid:
        print(f"Ваш номер {phone_number} соответствует узбекскому формату. ")
        return True
        
    else:
        print(f"Ваш номер {phone_number} не соответствует узбекскому формату.")
        return False
    



    


