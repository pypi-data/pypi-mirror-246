import re

def validate_number(phone_number):   
    phone_pattern = re.compile(r'^\+998\d{9}$')
    is_valid = bool(re.match(phone_pattern, phone_number))

    if is_valid:
        print(f"The phone number {phone_number} is in the Uzbek format.")
        return True
        
    else:
        print(f"The phone number {phone_number} is not in the Uzbek format.")
        return False

    


