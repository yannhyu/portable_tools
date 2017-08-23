from datetime import datetime
from dateutil.parser import parse

def is_date(string):
    try: 
        parse(string)
        return True
    except ValueError:
        return False

dob_str = '00/00/0000'
dob_str_2 = '03/01/1990'
empty_str = ''
none = 'Null'
impossible_leap_str = '02/29/2010'
valid_leap_str = '02/29/2016'
# dob = datetime.strptime( dob_str, "%m/%d/%Y" )
# print(dob)

# dob = datetime(0000, 00, 00)
# dob = dob.strftime("%Y-%m-%d")
print(is_date(dob_str))
print(is_date(dob_str_2))
print(is_date(empty_str))
print(is_date(none))
print(is_date(impossible_leap_str))
print(is_date(valid_leap_str))

more_date_strs = (
    '10/02/2009',
    '07 22 2009',
    '09-08-2008',
    '9-9/2008',
    '11/4 2010',
    '03/07-2009',
    '09-01 2010',
    '00/00/0000',
    '02/29/2010',
    '02/29/2016'
    )

for potential_date_str in more_date_strs:
    print('{} valid date?: {}'.format(potential_date_str, is_date(potential_date_str)))
