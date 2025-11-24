import pandas as pd

df = pd.read_csv('./data_csv/강원특별자치도_가축사육업.csv', encoding='cp949')

cols = pd.DataFrame({
    "index": range(len(df.columns)),
    "column_name": df.columns
})

cols
import pandas as pd

# 데이터 불러오기
df = pd.read_csv('./data_csv/강원특별자치도_가축사육업.csv', encoding='cp949')

# 인허가일자 문자열을 날짜로 변환
df['인허가일자'] = pd.to_datetime(df['인허가일자'], errors='coerce')

# 연도 추출
df['permit_year'] = df['인허가일자'].dt.year

# 폐업 여부 판단 → 영업상태명 사용
df['is_closed'] = df['영업상태명'] == '폐업'

# 연도별 총 업체 수
total_by_year = df.groupby('permit_year')['번호'].count()

# 연도별 폐업 수
closed_by_year = df.groupby('permit_year')['is_closed'].sum()

# 결과 합치기
result = pd.DataFrame({
    '총업체수': total_by_year,
    '폐업수': closed_by_year
})

# 폐업률 계산
result['폐업률(%)'] = (result['폐업수'] / result['총업체수'] * 100).round(2)

result
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'AppleGothic'
plt.rcParams['axes.unicode_minus'] = False
# 2. 계패업 비율 조사 하여 해당 연도까지의 위험 업종인지를 판단함. 
data_columns = df.columns[df.isnull().all()]
data_columns
df.drop(columns = data_columns, inplace = True)
df.info()