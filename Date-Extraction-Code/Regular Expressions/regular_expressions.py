"""
This function returns regular expressions for different languages.

Possible languages:
en = english
fr = french
de = german

"""

def reg_exp(languages = ['en']):
    

    ## Determine required languages ----

    languages = map(str.lower, languages)  # Ensure language identifiers are in lowercase

    I = [0, 0, 0]

    if 'en' in languages: I[0] = 1;
    if 'fr' in languages: I[1] = 1;
    if 'de' in languages: I[2] = 1;
    

    ## English (EN) ----

    months_EN = ['january', 'jan', 'february', 'feb', 'feby', 'march', 'mar', 'april', 'apr', 'apl', 'may', 'june', 'july', 'august', 'aug', 'september', 'septr', 'sept', 'sep', 'october', 'oct', 'november', 'nov', 'december', 'dec', 'decbr']
    dow_EN = ['monday', 'mon', 'tuesday', 'tues', 'tue', 'wednesday', 'wed', 'thursday', 'th', 'thurs', 'thu', 'friday', 'fri', 'saturday', 'sat', 'sunday', 'sun']


    ## French (FR) ----

    months_FR = ['janvier', 'janv', 'jan', 'fevrier', 'février', 'fevr', 'févr', 'fév', 'mars', 'mar', 'avril', 'avr', 'mai', 'juin', 'juillet', 'juil', 'juill', 'aout', 'août', 'septembre', 'sept', 'octobre', 'oct', 'novembre', 'nov', 'decembre', 'décembre', 'dec', 'déc']
    dow_FR = ['lundi', 'lun', 'mardi', 'mar', 'mercredi', 'mer', 'jeudi', 'jeu', 'vendredi', 'ven', 'samedi', 'sam', 'dimanche', 'dim']


    ## German (DE) ----

    months_DE = ['januar', 'jan', 'jän', 'februar', 'feb', 'marz', 'märz', 'april', 'apr', 'mai', 'juni', 'juli', 'august', 'aug', 'september', 'sept', 'oktober', 'okt', 'november', 'nov', 'dezember', 'dez']
    dow_DE = ['montag', 'mo', 'dienstag', 'di', 'mittwoch', 'mi', 'donnerstag', 'do', 'freitag', 'fr', 'samstag', 'sa', 'sonntag', 'so']

    
    ## Combining Languages ----

    month_re = I[0]*months_EN + I[1]*months_FR + I[2]*months_DE

    month_re = list(set(month_re))

    month_re = sorted(month_re, key = len, reverse = True)
                 
    dow_re = I[0]*dow_EN + I[1]*dow_FR + I[2]*dow_DE

    dow_re = list(set(dow_re))

    dow_re = sorted(dow_re, key = len, reverse = True)


    ## Final Regular Expressions ----

    date_re = r'\b([1-9]|[12][0-9]|3[01])(\b|th\b|rd\b|st\b|nd\b)'          #"\d{1,2}" #"([1-2][0-9]|30|31|[1-9])"

    date_re2 = r'\b([1-9]|[12][0-9]|3[01])(th\b|rd\b|st\b|nd\b)'
    month_num_re = r'\b([1-9]|[1][0-2])\b'
    
    #suffix_re = "(th|st|nd|rd)"

    date_minimal_re = "\d{1,2}"
    
    joins_re = "(\.|-|/|:)"

    dow_re = "(" + "|".join(dow_re) + ")"
    
    month_re = "(" + "|".join(month_re) + ")"

    year_re = "\d{2,4}"

    breaks_re = "(\.| |,)?( )"
    

    return (date_re, date_re2, month_num_re, date_minimal_re, month_re, year_re, dow_re, joins_re, breaks_re)
