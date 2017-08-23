import time
from datetime import datetime
from functools import partial
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.exc import DataError
from sqlalchemy.dialects.postgresql import \
    CHAR, VARCHAR, DATE, TIMESTAMP, INTEGER, BIGINT, NUMERIC
from coroutine import coroutine
from dateutil.parser import parse

def is_invalid_date(string):
    try: 
        parse(string)
        return False
    except ValueError:
        return True

# import psycopg2.extras
# psycopg2.extras.register_json(oid=3802, array_oid=3807, globally=True)

DB_URI = 'postgresql://u:p@host/database'
# engine = create_engine(DB_URI, echo=True)
engine = create_engine(DB_URI, echo=False)
TARGET_TBL_NAME = 'temp_batch_insurance0_unstaged_t'
metadata = MetaData(engine)
metadata.reflect(engine, only=[TARGET_TBL_NAME, 'unstaged_t',])
target_tbl = metadata.tables[TARGET_TBL_NAME]
TRUNCATION_WHITELIST = ['acctnum', 'hid', 'cpi']

def transform(rows, target):
    for row in rows:
        # print('id_rec:{} -- cust_id:{} -- our_run_date:{} -- fail_reason:{}'
        #     .format(row.id_rec, row.cust_id, row.our_run_date, row.fail_reason))
        dl = row.dataload
        dl['cust_id'] = row.cust_id
        dl['our_run_date'] = row.our_run_date
        dl['seqnum'] = row.seqnum
        # TODO: ask about the following fields
        dl['acctnum_seq'] = row.seqnum
        dl['client_npi1'] = ''
        dl['emdeon_billing_id'] = ''
        target.send(dl)

# to fix DataError regarding date with PostgreSQL
# invalid input syntax for type numeric: ""
# invalid input syntax for type date: ""
# date/time field value out of range: "00/00/0000"
def curate(dl):
    for column in target_tbl.columns:
        if isinstance(column.type, (DATE, NUMERIC)):
            if not dl.get(column.name):
                dl[column.name] = None
        if isinstance(column.type, DATE):
            date_str = dl.get(column.name)
            if date_str and is_invalid_date(date_str):
                dl[column.name] = None

    return dl

# A sink.  A coroutine that receives data & persists to db
@coroutine
def store2db():
    Base = automap_base(metadata=metadata)
    Base.prepare(engine, reflect=False)
    TempBatchIns0Unstaged = Base.classes.temp_batch_insurance0_unstaged_t
    session = Session(engine)
    while True:
        dl = (yield)
        print('{} {} {}'.format(dl.get('fname'), dl.get('mname'), dl.get('lname')))
        # print(dl)
        # to fix DataError regarding date with PostgreSQL
        dl = curate(dl)
        session.add(TempBatchIns0Unstaged(**dl))

        print('----- before commit ----')
        try:
            session.commit()
            print('----- after commit ----')          
        except DataError as exc:
            session.rollback()
            reason = exc.message
            print('Data Error: {}'.format(reason))           

        # except Exception as inst:
        #    session.rollback()
        #    print(inst.statement % inst.params)                    

# convenient methods
def fixed_size_str(somestring, maxlength):
    return str(somestring)[:maxlength]

def generate_truncation_map():
    fld_map = dict()
    for column in target_tbl.columns:
        if isinstance(column.type, VARCHAR):
            fld_map[column.name] = partial(fixed_size_str, maxlength=column.type.length)
        else:
            fld_map[column.name] = None
    return fld_map

def trucation_exclusion(truncation_map, keys2exclude):
    for k in keys2exclude:
        truncation_map[k] = None
    return truncation_map    

@coroutine
def truncate(trunc, target):
    while True:
        dl = (yield)
        # dl_truncated = {k:(trunc[k](v) if trunc.get(k) else v) for k, v in dl.iteritems()}
        # target.send(dl_truncated)
        for k in trunc:
            if trunc.get(k) and k in dl:
                dl[k] = trunc[k](dl[k])
        target.send(dl)


if __name__ == '__main__':
    overall_start_time = time.time()
    result = engine.execute('select * from unstaged_t')
    truncation_map = generate_truncation_map()
    truncation_map_adjusted = trucation_exclusion(truncation_map, 
                                                  TRUNCATION_WHITELIST)
    transform(result,
              truncate(truncation_map_adjusted,
              store2db()))
    print("Overall: --- {} seconds ---".format(time.time() - overall_start_time))