import pandas as pd

df = pd.read_csv('program_L2.csv')

#print(bring_it)

max_size = df['Size'].max()

print(max_size)

# https://stackoverflow.com/questions/35577092/pandas-find-max-value-in-column-and-print-its-row

#print list(df.loc[df['xrb'][::-1].idxmax()])

just_the_row = (df.loc[df['Size'][::-1].idxmax()])
print(just_the_row)

