import phonenumbers
from geopy.geocoders import Nominatim

def get_country_name(phone_number):
    try:
        parsed_number = phonenumbers.parse(phone_number, None)
        region_code = phonenumbers.region_code_for_number(parsed_number)

        if region_code:
            geolocator = Nominatim(user_agent="get_country_name")
            location = geolocator.country(region_code.upper())
            country_name = location.address
            return country_name
        else:
            return "Unknown"
    except phonenumbers.NumberParseException:
        return "Invalid Format"

