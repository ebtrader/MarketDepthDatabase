
import time
import datetime
import pandas as pd

from DBHelperGoosev3 import DBHelper

db = DBHelper()
df = db.getDataInPandaDF()

dfobj = df
print (dfobj)

