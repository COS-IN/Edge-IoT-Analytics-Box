import datetime
from dateutil import parser 

def t_minus_delta( t, delta ): 
    delta = datetime.timedelta( seconds=delta )
    e = t - delta
    return e

def convert_to_iso( date_str ):
    if isinstance( date_str, str ): 
        local_time = parser.parse(date_str) 
    else:
        local_time = date_str
    utc_time = local_time.astimezone(datetime.timezone.utc)
    iso_8601_string = utc_time.isoformat()
    return iso_8601_string
def convert_to_isodatetime( date_str ): 
    s = convert_to_iso( date_str )
    return parser.parse(s) 

def apply_delta( date_str, delta ):
    utc_time = parser.parse(date_str) 
    val = int(delta[:-1]) 
    t = delta[-1]
    if t == 'h':
        timedelta = datetime.timedelta( hours=val )
    elif t == 'm':
        timedelta = datetime.timedelta( minutes=val )
    elif t == 's':
        timedelta = datetime.timedelta( seconds=val )
    utc_time = utc_time - timedelta 
    utc_time = utc_time.astimezone(datetime.timezone.utc)
    iso_8601_string = utc_time.isoformat()
    return iso_8601_string
