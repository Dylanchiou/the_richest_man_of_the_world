import os
import pandas as pd
import glob
folder_path = '/Users/dylan/Desktop/無限學院講義/專案構想/世界最富有的人'
csv_files = glob.glob(os.path.join(folder_path, 'Top_10_richest_*.csv'))
df_list = []
for file in csv_files:
    year = int(os.path.basename(file).split('_')[3].split('.')[0])
    df = pd.read_csv(file)
    df['year'] = year
    df['rank'] = df.index + 1
    df_list.append(df)
combined_df = pd.concat(df_list, ignore_index=True)
combined_df = combined_df.sort_values(by=['year', 'rank']).reset_index(drop=True)
combined_df.drop('Unnamed: 0', axis=1)
output_file_path = os.path.join(folder_path, 'data_1996_2024.csv')
combined_df.to_csv(output_file_path, index=False)

def convert_money_string(money_str):
    money_str = money_str.replace('$', '').replace(',', '').strip()
    if 'billion' in money_str:
        return int(float(money_str.replace('billion', '').strip()) * 1e9)
    elif 'million' in money_str:
        return int(float(money_str.replace('million', '').strip()) * 1e6)
    elif 'thousand' in money_str:
        return int(float(money_str.replace('thousand', '').strip()) * 1e3)
    else:
        return int(float(money_str))
combined_df['Net_worth_USD'] = combined_df['Net_worth_USD'].apply(convert_money_string)
combined_df.to_csv(output_file_path, index=False)
#純測試圖片，這個圖沒意義
# import matplotlib.pyplot as plt
# x = combined_df['year']
# y = combined_df['Net_worth_USD']
# fig = plt.figure(figsize=(12, 4))
# ax = fig.add_subplot()
# ax.plot(x, y)
# ax.ticklabel_format(axis = 'y', style = 'sci', scilimits = (-3, 3))
# plt.show()
import numpy as np
# print(f'數據大小: {combined_df.shape}')

#增加四個欄位：各個年份的中位數、平均數、最大值、最小值
combined_df['Median'] = None
combined_df['Mean'] = None
combined_df['Max'] = None
combined_df['Min'] = None
for start in range(0, len(combined_df), 10):
    end = start + 10
    year_slice = combined_df[start : end]
    median = year_slice['Net_worth_USD'].median()
    mean = year_slice['Net_worth_USD'].mean()
    max_value = year_slice['Net_worth_USD'].max()
    min_value = year_slice['Net_worth_USD'].min()
    combined_df.loc[start : end, 'Median'] = median
    combined_df.loc[start : end, 'Mean'] = mean
    combined_df.loc[start : end, 'Max'] = max_value
    combined_df.loc[start : end, 'Min'] = min_value
output_file_path = '/Users/dylan/Desktop/無限學院講義/專案構想/世界最富有的人/data_1996_2024_new.csv'
combined_df.to_csv(output_file_path, index = False)

df1 = pd.read_csv('/Users/dylan/Desktop/無限學院講義/專案構想/世界最富有的人/data_1996_2024_new.csv')
# print(df1.columns)
import matplotlib.pyplot as plt
fig, ax = plt.subplots(facecolor = 'white')
x = df1['year']
y1 = df1['Median']
y2 = df1['Mean']
y3 = df1['Max']
y4 = df1['Min']
fig = plt.figure(figsize = (12, 4))
ax = fig.add_subplot()
ax.plot(x, y1, 'b', label = 'Median')
ax.plot(x, y2, 'r', label = 'Mean')
ax.plot(x, y3, 'y', label = 'Max')
ax.plot(x, y4, 'g', label = 'Min')
ax.set_title('annual trends')
ax.legend(loc = 3)
plt.savefig('圖一.png', dpi = 300, facecolor = fig.get_facecolor(), transparent = True)
plt.show()

#統計每年上榜國家，一年計算一次，加起來會是289
# national_counts = df1['Nationality'].value_counts()
# print(national_counts)

#改以每五年統計一次
result_df = pd.DataFrame()
for start_year in range(1996, 2025, 5):
    end_year = start_year + 4
    period_df = df1[(df1['year'] >= start_year) & (df1['year'] <= end_year)]
    country_counts = period_df['Nationality'].value_counts().reset_index()
    country_counts.columns = ['Nationality', 'Counts']
    country_counts['Period'] = f"{start_year} - {end_year}"
    result_df = pd.concat([result_df, country_counts], ignore_index=True)
# print(result_df)

#每五年統計一次各個國家上榜佔比-圓餅圖
periods = result_df['Period'].unique()
fig, axs = plt.subplots(3, 2, figsize = (15, 15))
axs = axs.flatten()
for i, period in enumerate(periods):
    ax = axs[i]
    period_data = result_df[result_df['Period'] == period]
    ax.pie(period_data['Counts'], labels = period_data['Nationality'], autopct = '%1.1f%%', startangle = 140)
    ax.set_title(f"{period} POC")
plt.tight_layout()
plt.savefig('圖二.png', dpi = 300, facecolor = fig.get_facecolor(), transparent = True)
plt.show()

#計算私人資產來源次數
# Primary_source_counts = df1['Primary_source_of_wealth'].value_counts()
# print(Primary_source_counts)

#觀察1996-2024，私人資產來源變化的趨勢-長條圖
result_df = pd.DataFrame()
for year in range(1996, 2025):
    period_df = df1[df1['year'] == year]
    source_counts = period_df['Primary_source_of_wealth'].value_counts().reset_index()
    source_counts.columns = ['Primary_source_of_wealth', 'Count']
    source_counts['year'] = year
    result_df = pd.concat([result_df, source_counts], ignore_index = True)

#篩選出現次數前15名產業
top_source = result_df['Primary_source_of_wealth'].value_counts().nlargest(15).index
filtered_df = result_df[result_df['Primary_source_of_wealth'].isin(top_source)]
pivot_df = filtered_df.pivot(index = 'year', columns = 'Primary_source_of_wealth', values = 'Count').fillna(0)

pivot_df.plot(kind = 'bar', stacked = True, figsize = (15, 10), colormap = 'tab20')
plt.title('CIIT 1996-2024')
plt.xlabel('Year')
plt.ylabel('Primary_source')
plt.legend(loc = 'upper right', bbox_to_anchor = (1.2, 1))
plt.tight_layout()
plt.savefig('圖三.png', dpi = 300, facecolor = fig.get_facecolor(), transparent = True)
plt.show()