
import time
import datetime
import pandas as pd

from DBHelperGoosev3 import DBHelper

db = DBHelper()
df = db.getDataInPandaDF()
#dfobj = df['POSITION', 'SIZE']
#print (dfobj)

#df_new = df[['POSITION', 'SIZE', 'Side', 'Price']]
#print(df_new)
just_the_row = (df.loc[df['SIZE'][::-1].idxmax()])
print(just_the_row)
