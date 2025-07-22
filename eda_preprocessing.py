import pandas as pd

# ===== 1. 산업단지 데이터 로딩 및 전처리 (xlsx 사용) =====
df_industry = pd.read_excel(r"C:\mini_project\산업단지현황조사_2023년 4분기.xlsx", sheet_name="시도별", skiprows=1)
industry_cols = df_industry.iloc[:, [0, 1, 2]]
industry_cols.columns = ["시도", "단지수", "지정면적"]

# '소계', '계', '합계' 제거
def is_valid_region(name):
    if isinstance(name, str):
        if any(x in name for x in ["소계", "계", "합계"]):
            return False
        return True
    return False

industry_clean = industry_cols[industry_cols["시도"].apply(is_valid_region)].copy()
industry_clean = industry_clean.reset_index(drop=True)

# 시도명 정제
def extract_sido_fixed(name):
    if isinstance(name, str):
        if name.startswith(('서울', '부산', '대전', '대구', '광주', '울산', '인천', '세종')):
            return name[:2]
        return name[:3]
    return None

industry_clean["시도"] = industry_clean["시도"].apply(extract_sido_fixed)
industry_clean["단지수"] = pd.to_numeric(industry_clean["단지수"], errors="coerce")
industry_clean["지정면적"] = pd.to_numeric(industry_clean["지정면적"], errors="coerce")
industry_grouped = industry_clean.groupby("시도")[["단지수", "지정면적"]].sum().reset_index()

# ===== 2. 인구밀도 데이터 로딩 및 전처리 =====
df_population = pd.read_excel(r"C:\mini_project\지역별_인구밀도.xlsx", sheet_name="Sheet0", skiprows=2)
pop_cols = df_population.iloc[:, [0, 1]]
pop_cols.columns = ["시도", "인구밀도"]
pop_clean = pop_cols.dropna().reset_index(drop=True)

valid_sido = [
    '서울', '부산', '대구', '인천', '광주', '대전', '울산', '세종',
    '경기', '강원', '충북', '충남', '전북', '전남', '경북', '경남', '제주'
]
pop_filtered = pop_clean[pop_clean["시도"].isin(valid_sido)].copy()
pop_filtered["인구밀도"] = pop_filtered["인구밀도"].astype(str).str.replace(",", "")
pop_filtered["인구밀도"] = pd.to_numeric(pop_filtered["인구밀도"], errors="coerce")

# ===== 3. 산업단지 + 인구밀도 병합 =====
df_region = industry_grouped.merge(pop_filtered, on="시도", how="inner")

# ===== 4. 미세먼지 등급 일수 데이터 병합 =====
df_pm = pd.read_excel(r"C:\mini_project\시도별_미세먼지_등급별_일수.xlsx", skiprows=1)
df_pm = df_pm.rename(columns={
    df_pm.columns[0]: "시도",
    "Unnamed: 7": "PM10_좋음", "Unnamed: 8": "PM10_보통",
    "Unnamed: 13": "PM25_좋음", "Unnamed: 14": "PM25_보통"
})
df_pm = df_pm[["시도", "PM10_좋음", "PM10_보통", "PM25_좋음", "PM25_보통"]]
df_pm["시도"] = df_pm["시도"].str.strip()
df_region = df_region.merge(df_pm, on="시도", how="left")

# ===== 5. 산업단지 면적 비율 계산 =====
area_km2 = {
    '서울': 605.21, '부산': 770.07, '대구': 883.48, '인천': 1062.88,
    '광주': 501.24, '대전': 539.83, '울산': 1056.86, '세종': 465.23,
    '경기': 10172.57, '강원': 16873.52, '충북': 7417.72, '충남': 8246.64,
    '전북': 8069.17, '전남': 12258.14, '경북': 19029.65, '경남': 10534.77,
    '제주': 1849.06
}

def calc_ratio(row):
    area = area_km2.get(row['시도'], None)
    if area:
        지정면적_m2 = row['지정면적'] * 1000  # 천㎡ → ㎡
        전체면적_m2 = area * 1_000_000       # ㎢ → ㎡
        return (지정면적_m2 / 전체면적_m2) * 100
    else:
        return None

df_region["산업단지_면적비율"] = df_region.apply(calc_ratio, axis=1)

# ===== 6. 대기오염물질 농도 (2023년) 병합 =====
df_pollution = pd.read_csv(r"C:\mini_project\시도별_대기오염물질_2023.csv", encoding="utf-8-sig")
df_pollution["시도"] = df_pollution["시도"].str.strip()
df_region = df_region.merge(df_pollution, on="시도", how="left")

# ===== 7. 저장 =====
df_region.to_csv(r"C:\mini_project\merged_region_data_final.csv", index=False, encoding="utf-8-sig")
print("✅ 병합 완료! 저장된 파일: merged_region_data_final.csv")