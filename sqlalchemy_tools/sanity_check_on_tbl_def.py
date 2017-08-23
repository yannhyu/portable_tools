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
metadata.reflect(engine, only=['temp_batch_insurance0_unstaged_t',
                               'read_insurance0_v1_t',
                               'read_insurance0_v2_t',
                               'read_insurance0_v2_invoice_t',
                               'read_insurance0_v3_t',
                               'read_insurance0_v3_invoice_t',
                               'read_insurance0_v4_t',
                               'read_insurance0_v4_invoice_t',
                               'read_insurance0_v5_t',
                               'read_insurance0_v6_t',])
target_table = metadata.tables['temp_batch_insurance0_unstaged_t']
# for column in target_table.columns:
#     print('{} -- {}'.format(column.name, column.type))

target_tbl_cols_names = [column.name for column in target_table.columns]
#print(target_tbl_cols_names)

v1_table = metadata.tables['read_insurance0_v1_t']
v1_tbl_cols_names = [column.name for column in v1_table.columns]
#print(v1_tbl_cols_names)

v2_table = metadata.tables['read_insurance0_v2_t']
v2_tbl_cols_names = [column.name for column in v2_table.columns]
#print(v2_tbl_cols_names)

v3_table = metadata.tables['read_insurance0_v3_t']
v3_tbl_cols_names = [column.name for column in v3_table.columns]
#print(v3_tbl_cols_names)

v4_table = metadata.tables['read_insurance0_v4_t']
v4_tbl_cols_names = [column.name for column in v4_table.columns]
#print(v4_tbl_cols_names)

v5_table = metadata.tables['read_insurance0_v5_t']
v5_tbl_cols_names = [column.name for column in v5_table.columns]
#print(v5_tbl_cols_names)

v6_table = metadata.tables['read_insurance0_v6_t']
v6_tbl_cols_names = [column.name for column in v6_table.columns]
#print(v6_tbl_cols_names)

bigger = set(target_tbl_cols_names)
small_v1 = set(v1_tbl_cols_names)
small_v2 = set(v2_tbl_cols_names)
small_v3 = set(v3_tbl_cols_names)
small_v4 = set(v4_tbl_cols_names)
small_v5 = set(v5_tbl_cols_names)
small_v6 = set(v6_tbl_cols_names)
print(small_v1.issubset(bigger))
print(small_v2.issubset(bigger))
print(small_v3.issubset(bigger))
print(small_v4.issubset(bigger))
print(small_v5.issubset(bigger))
print(small_v6.issubset(bigger))

print('************************')
print(small_v5 - bigger)


