import pycountry

def iso_to_country_name(iso_code):
    try:
        if iso_code == 'EU': return "European Union" 
        elif iso_code == 'WEF': return "World Economic Forum"
        elif iso_code == 'OECD': return "OECD"
        elif iso_code == 'UN': return "United Nations"
        elif iso_code == 'UAE': return "United Arab Emirates"
        else: return pycountry.countries.get(alpha_3=iso_code).name

    except AttributeError:
        raise Exception("Invalid country ISO_3 code")

def country_name_to_iso(country_name: str):
    country = pycountry.countries.get(name=country_name)

    if country:
        iso_3_letter_code = country.alpha_3
        return iso_3_letter_code

    return None