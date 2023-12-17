import re
import phonenumbers
def validate_number(phone_number):     
    uzbek_pattern = re.compile(r'^\+998\d{9}$')
    if re.match(uzbek_pattern, phone_number):
        print(f"Ваш номер {phone_number} соответствует узбекскому формату.")
        return True, "Uzbekistan"
    
    try:
        # Парсинг номера с использованием библиотеки phonenumbers
        parsed_number = phonenumbers.parse(phone_number, None)
        country_info = phonenumbers.region_code_for_number(parsed_number)
        country_name = phonenumbers.region_name_for_number(parsed_number)
        print(f"Ваш номер {phone_number} соответствует формату страны: {country_name}.")
        return True, country_name
    except phonenumbers.NumberFormatException:
        print(f"Не удалось определить страну для номера {phone_number}.")
        return False, "Unknown"

    


