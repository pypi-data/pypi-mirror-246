import re


def count_et_al(text):
    count = text.lower().count('et al')
    return count


def find_years(text):
    found = [x.group() for x in re.finditer( r'(?<!\d|\w)(19[7-9][0-9]|20[0-2][0-9])(?!\d|\w)', text)]
    return found if len(found) > 0 else []


def find_authors(text):
    found = [x.group() for x in re.finditer( r"((?<!([A-Ž]\.\s))(([A-Ž][a-ž]+\,\s))([A-Ž]\.)([A-Ž]\.)?)|((?<!([A-z]\.\s))(?:[A-Z]\.\s)(?:[A-Z]\.\s)?[A-Z][a-z]+)", text)]
    return found if len(found) > 0 else []
def find_pp(text):
    found = [x.group() for x in re.finditer( r"(PP|Pp|pp)\.", text)]
    return found if len(found) > 0 else []

def find_vol(text):
    found = [x.group() for x in re.finditer( r"(vol|Vol|VOL)\.", text)]
    return found if len(found) > 0 else []

def find_available_at(text):
    found = [x.group() for x in re.finditer( r"([A|a]vailable\sat)|([A|a]ccessed on)|([R|r]etrieved from)|([A|a]ccessed\s\d{1,2})", text)]
    return found if len(found) > 0 else []

def find_http(text):
    found = [x.group() for x in re.finditer( r"http", text)]
    return found if len(found) > 0 else []

def calc_score(text):
    n_authors = (len(find_authors(text)))
    n_years = (len(find_years(text)))
    n_et_al = (count_et_al(text))
    n_pp = (len(find_pp(text)))
    n_vol = (len(find_vol(text)))
    n_available_at = (len(find_available_at(text)))
    n_http = (len(find_http(text)))

    return [n_authors, n_years, n_et_al, n_pp, n_vol, n_available_at, n_http]

def classify_text(score):
    label = '?'

    if score[0] > 0:
        label = 'FR'
    elif score[6] > 0:
        label = 'FR'
    elif score[0] == 0 and score[2] == 0 and score[3] == 0:
        label = 'FT'
    elif score[1] > 0 and score[5] > 0:
        label = 'FR'
    elif score[2] > 0:
        label = 'FR'

    return label
