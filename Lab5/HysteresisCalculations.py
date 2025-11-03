import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
#importing in the csv file, editing columns for processing and separating tests 1-4
raw = pd.read_csv('lab5_testingDataRaw - Lab5.csv')

mat_properties = {
    'aluminum': [9.54, 27.76],
    'steel': [9.78, 27.34],
    'nylon': [43.26, 83.06],
}

test_material_order = [
    "aluminum",
    "aluminum",
    "nylon",
    "nylon",
    "steel",
    "steel",
    "steel",
    "steel",
    "nylon",
    "nylon",
    "nylon",
    "nylon",
]

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
tests = [test1, test2, test3, test4, test5,test6,test7,test8,test9,test10,test11,test12]

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
for test in tests:
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
results = []
test1_overview = peaks_and_valleys.iloc[0:6]
test2_overview = peaks_and_valleys.iloc[6:14]
test3_overview = peaks_and_valleys.iloc[14:22]
test4_overview = peaks_and_valleys.iloc[22:30]
test5_overview  = peaks_and_valleys.iloc[30:36]
test6_overview  = peaks_and_valleys.iloc[36:40]
test7_overview  = peaks_and_valleys.iloc[40:44]
test8_overview  = peaks_and_valleys.iloc[44:48]
test9_overview  = peaks_and_valleys.iloc[48:52]
test10_overview = peaks_and_valleys.iloc[52:56]
test11_overview = peaks_and_valleys.iloc[56:60]
test12_overview = peaks_and_valleys.iloc[60:64]

overviews = [test1_overview,test2_overview,test3_overview,test4_overview,test5_overview,test6_overview,
             test7_overview,test8_overview,test9_overview,test10_overview,test11_overview,test12_overview]
def rlx_pct(data,col):
    return (pd.to_numeric(data[col].iloc[1]) - pd.to_numeric(data[col].iloc[-1]))/pd.to_numeric(data[col].iloc[1])

for i in overviews:
    rlx_pct(i,'load')
    print(f"test {i}: {rlx_pct(i,'load')*100}% stress relaxation")

def getStressStrain(test,mat):
    area = mat_properties[mat][0]
    length = mat_properties[mat][1]
    test=test.copy()
    test['load']=pd.to_numeric(test['load'], errors='coerce')
    test['disp']=pd.to_numeric(test['disp'], errors='coerce')
    test['stress'] = test['load']/area
    test['strain']=test['disp']/length
    return test


for i, test in enumerate(tests):
    mat=test_material_order[i]
    tests[i] = getStressStrain(test,mat)

for i in range(0,len(tests)):
    tests[i]['cycle'] = pd.to_numeric(tests[i]['cycle'], errors='coerce')

    
    cyclecut = round(len(tests[i])/(tests[i]['cycle'].max()+1))
    # we can assume cycles are done at even rates, so fractions of the cycle can be approximated
    # to cycle start/stop times 
    tests[i]=getStressStrain(tests[i],test_material_order[i])
    a = np.trapezoid(tests[i]['stress'].iloc[0:cyclecut],
                     tests[i]['strain'].iloc[0:cyclecut])
    b = np.trapezoid(tests[i]['stress'].iloc[-cyclecut:],
                     tests[i]['strain'].iloc[-cyclecut:])
    result = a-b
    print((a,b))
    print(f"test {i+1} value: {abs(result)}")

    results.append(result)
    
""" section commented out for improved speed, uncomment to visualize the data
fig, axes = plt.subplots(4,3,figsize=(8,6))
axes=axes.flatten()
fig2, axes2 = plt.subplots(4, 3, figsize=(8,6))
axes2 = axes2.flatten()
plt.tight_layout()
for i, test in enumerate(tests): 
    axes[i].plot(tests[i]['strain'], tests[i]['stress'])
    axes[i].set_title(f"Test {i+1} ({mat})")
    axes[i].set_xlabel("Strain (mm/mm)")
    axes[i].set_ylabel("Stress (N/mm²)")
    axes[i].grid(True)

for i, test in enumerate(tests):
    mat = test_material_order[i]
    # Already processed for stress, but force vs time uses raw 'load' and 'time'
    axes2[i].plot(test['time'], test['load'], label="Force-Time", color='orange')
    axes2[i].set_title(f"Test {i+1} ({mat})")
    axes2[i].set_xlabel("Time (s)")
    axes2[i].set_ylabel("Force (N)")
    axes2[i].grid(True)

plt.tight_layout()
plt.show()
"""