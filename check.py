import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler

# CSV 파일 읽기
xls_path = r'./raw_files/대기농도.xlsx'
df = pd.read_excel(xls_path)
print(df.columns)
# print(df[df['Processing Method'].isnull()]['Processing Method'])
