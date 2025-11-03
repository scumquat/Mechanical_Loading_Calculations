import pandas as pd
import numpy as np
#importing in the csv file, editing columns for processing and separating tests 1-4
raw = pd.read_csv('lab5_testingDataRaw - Lab5.csv')

columns = ['cycle','disp','load','time']
raw.columns = columns
test1 = raw.iloc[7:528]
test2 = raw.iloc[539:1069]
test3 = raw.iloc[1078:2000]
test4 = raw.iloc[2009:3891]
test5 = raw.iloc[3900:5205]
test6 = raw.iloc[5214:6391]
test7= raw.iloc[6400:7075]
test8 = raw.iloc[7085:7843]
test9 = raw.iloc[7852:8631]
test10 = raw.iloc[8640:9323]
test11 = raw.iloc[9332:10280]
test12 = raw.iloc[10289:11152]
# separated tests in a list for iterating
tests = [test1, test2, test3, test4]
tests2 = [test5,test6,test7,test8,test9,test10,test11,test12]

# split the separated tests into a list of cycles
def separate_cycles(data):
 
    cycle_list = []
    for cycle_number, group in data.groupby('cycle'):
        cycle_list.append(group.copy())
    return cycle_list

# function that returns the maximum and minimums of a dataframe based on specified column
def minmax(data, column):

    data_sorted = data.sort_values(by=column)
    return data_sorted.iloc[[0, -1]]

# output holder
output = []

# iterator
for test in tests+tests2:
    # split the test into cycles
    cycles = separate_cycles(test)
    
    # process each cycle to get first and last rows, and add the output to the holder
    for cycle in cycles:
        result = minmax(cycle, 'disp')
        output.append(result)

# combine results into one dataframe with peaks and valleys for each test sample
peaks_and_valleys = pd.concat(output, ignore_index=True)
# display results 
print(peaks_and_valleys)

test1_overview = peaks_and_valleys.iloc[0:6]
test2_overview = peaks_and_valleys.iloc[6:14]
test3_overview = peaks_and_valleys.iloc[14:22]
test4_overview = peaks_and_valleys.iloc[22:30]

overviews = [test1_overview,test2_overview,test3_overview,test4_overview]
def rlx_pct(data,col):
    return (pd.to_numeric(data[col].iloc[1]) - pd.to_numeric(data[col].iloc[-1]))/pd.to_numeric(data[col].iloc[1])

for i in overviews:
    rlx_pct(i,'load')
    print(f"{rlx_pct(i,'load')*100}% stress relaxation")

