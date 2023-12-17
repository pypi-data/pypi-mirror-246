import re
import phonenumbers
def validate_number(phone_number):     
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        if not phonenumbers.is_valid_number(parsed_number):
            print(f"Ваш номер {phone_number} не соответствует формату.")
            return False, "Invalid Format"

        country_info = phonenumbers.region_code_for_number(parsed_number)
        country_name = phonenumbers.region_name_for_number(parsed_number)
        print(f"Ваш номер {phone_number} соответствует формату страны: {country_name}.")
        return True, country_name
    except phonenumbers.NumberFormatException:
        print(f"Не удалось определить страну для номера {phone_number}.")
        return False, "Unknown"
    


