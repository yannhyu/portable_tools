import time
from random import randint
import fileinput
from functools import partial
from decimal import Decimal
from datetime import datetime
from collections import namedtuple
import logging
import warnings
from sqlalchemy import exc as sa_exc
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.dialects.postgresql import \
    CHAR, VARCHAR, DATE, TIMESTAMP, INTEGER, BIGINT, NUMERIC

DB_URI = 'postgresql://u:p@host/database'
engine = create_engine(DB_URI)
metadata = MetaData(engine)
metadata.reflect(engine, only=['temp_batch_insurance0_unstaged_t',])
ex_table = metadata.tables['temp_batch_insurance0_unstaged_t']
for column in ex_table.columns:
    try:
        print('{} -- {} -- {}'.format(column.name, column.type, column.type.length))
    except AttributeError as aerr:
        print('{} -- {}'.format(column.name, column.type))