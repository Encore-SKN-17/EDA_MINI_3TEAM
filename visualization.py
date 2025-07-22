import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import platform

# 한글 폰트 설정
plt.rc('font', family='Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False

# ===== 데이터 불러오기 =====
df = pd.read_csv(r"C:\mini_project\merged_region_data_final.csv")

# ===== 전처리: 오염물질 수치 정제 =====
pollutants = ['SO2', 'NO2', 'O3', 'CO', 'PM10', 'PM2.5']
for col in pollutants:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# ===== 1. 변수 간 상관관계 히트맵 =====
plt.figure(figsize=(12, 8))
sns.heatmap(df.corr(numeric_only=True), annot=True, fmt=".2f", cmap="coolwarm")
plt.title("변수 간 상관관계 히트맵")
plt.tight_layout()
plt.savefig(r"C:\mini_project\Figure_상관관계_히트맵.png")
plt.show()

# ===== 2. 산업단지 면적비율 vs 대기오염물질 산점도 + 회귀선 =====
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
pollutants_subset = ['SO2', 'NO2', 'O3', 'CO']
for ax, pol in zip(axs.flatten(), pollutants_subset):
    sns.regplot(data=df, x='산업단지_면적비율', y=pol, ax=ax, scatter_kws={"s": 60})
    ax.set_title(f"🏭 산업단지 면적비율 vs {pol}")
plt.tight_layout()
plt.savefig(r"C:\mini_project\Figure_산업단지면적비율_대기오염물질.png")
plt.show()

# ===== 3. 인구밀도 vs 미세먼지 등급 산점도 =====
fig, axs = plt.subplots(2, 2, figsize=(14, 10))
dust_cols = ['PM10_좋음', 'PM10_보통', 'PM25_좋음', 'PM25_보통']
for ax, dust in zip(axs.flatten(), dust_cols):
    sns.regplot(data=df, x='인구밀도', y=dust, ax=ax, scatter_kws={"s": 60})
    ax.set_title(f"👥 인구밀도 vs {dust}")
plt.tight_layout()
plt.savefig(r"C:\mini_project\Figure_인구밀도_미세먼지등급.png")
plt.show()

# ===== 4. 지역별 미세먼지 등급 stacked bar chart =====
df_dust = df[['시도'] + dust_cols].set_index("시도")
df_dust.plot(kind='bar', stacked=True, figsize=(16, 8))
plt.title("시도별 미세먼지 등급 일수")
plt.ylabel("일수")
plt.xlabel("시도")
plt.tight_layout()
plt.savefig(r"C:\mini_project\Figure_지역별_미세먼지_StackedBar.png")
plt.show()