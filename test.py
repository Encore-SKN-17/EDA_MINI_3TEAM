import pandas as pd
import numpy as np

def table_reader(xls_path, header, end=None, sheet=None): 
    if sheet is not None:
        df = pd.read_excel(xls_path, header=header, sheet_name=sheet)
    else:
        df = pd.read_excel(xls_path, header=header)
    if end is not None:
        df = df.iloc[:end]
    return df

# 대기오염물질별 농도
so2 = table_reader('raw_files/대기농도.xlsx', header=3, end=19)
no2 = table_reader('raw_files/대기농도.xlsx', header=25, end=19)
o3 = table_reader('raw_files/대기농도.xlsx', header=47, end=19)
co = table_reader('raw_files/대기농도.xlsx', header=69, end=19)
filtered_so2 = so2[["연도", "'23년"]]
filtered_no2 = no2[["연도", "'23년"]]
filtered_o3 = o3[["연도", "'23년"]]
filtered_co = co[["연도", "'23년"]]
print('############################ co #######################################')
print(so2.columns)
print(filtered_so2)

# 미세먼지 등급
pm10 = table_reader('raw_files/시도별_미세먼지_등급별_일수.xlsx', header=[4,5], end=19)
pm25 = table_reader('raw_files/시도별_미세먼지_등급별_일수.xlsx', header=[27,28], end=19)
filtered_pm10 = pm10[[('좋음','2023년'), ('보통','2023년'), ('나쁨','2023년'), ('매우나쁨','2023년')]]
filtered_pm25 = pm25[[('좋음','2023년'), ('보통','2023년'), ('나쁨','2023년'), ('매우나쁨','2023년')]]
print('############################# filtered_pm25 #####################################')
print(filtered_pm25)

# 인구밀도
population = table_reader('raw_files/지역별_인구밀도.xlsx', header=[2,3], end=19)
filtered_pop = population[[('Unnamed: 0_level_0', 'Unnamed: 0_level_1'), ('2023', '인구'), ('2023', '인구밀도')]]
print('############################### filtered_pop ####################################')
print(filtered_pop)

# 산업단지 현황
industry = table_reader('raw_files/산업단지현황조사_2023년 4분기.xlsx', header=[6,7], sheet=1)
cleaned_industry = industry[[('구분', 'Unnamed: 0_level_1'), ('단지수', 'Unnamed: 1_level_1'), ('지정면적', 'Unnamed: 2_level_1'), ('관리면적', 'Unnamed: 3_level_1'), ('산업시설구역', '전체면적')]]
filtered_industry = cleaned_industry[cleaned_industry[('구분', 'Unnamed: 0_level_1')].str.contains('소계')]
filtered_industry['면적비율'] = filtered_industry[('지정면적', 'Unnamed: 2_level_1')] / filtered_industry[('산업시설구역', '전체면적')]
print('################################# filtered_industry ##################################')
print(filtered_industry)