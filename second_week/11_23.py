import pandas as pd
import os

# 1. 파일 경로 설정 및 확인
# '__file__'은 일반 Python 스크립트에서 현재 파일 경로를 제공합니다.
# 주피터/Colab 환경에서는 'os.getcwd()'를 사용할 수도 있습니다.
try:
    # 일반 .py 파일 실행 시
    base_dir = os.path.dirname(os.path.abspath(__file__)) 
except NameError:
    # 주피터 노트북/IPython 환경 시 (현재 작업 디렉토리)
    base_dir = os.getcwd() 

# 'data_csv' 폴더와 파일명을 결합하여 완전한 경로를 생성
file_path = os.path.join(base_dir, 'data_csv', '강원특별자치도_일반음식점.csv')

print(f"시도할 파일 경로: {file_path}")

# 2. 파일 존재 여부 확인 (디버깅)
if not os.path.exists(file_path):
    print("\n🚨 경로에 파일이 존재하지 않습니다. 폴더 이름이나 파일명이 정확한지 확인하세요.")
    # 경로가 잘못되었을 가능성이 높으므로 여기서 함수를 종료하거나 대체 경로를 시도해야 합니다.
else:
    # 3. 파일 읽기 (원래 시도했던 CP949 인코딩 사용)
    try:
        data = pd.read_csv(file_path, encoding='CP949', low_memory=False)
        print("✅ 파일 로드 성공!")
        data_columns = list(data.columns)
        # print(data_columns)

    except UnicodeDecodeError:
        print("\n⚠️ CP949 인코딩 오류 발생! UTF-8로 다시 시도합니다.")
        data = pd.read_csv(file_path, encoding='utf-8', low_memory=False)
        data_columns = list(data.columns)
data.info()
import numpy as np
total_size = data['폐업일자'].isnull().size
total_size
def make_autopct_with_ccount(pct):
    absolute_count = int(np.round(pct*total_size/100))
    return f"{pct:.1f}%\n({absolute_count}명)"
import pandas as pd
import matplotlib.pyplot as plt

plt.rc('font', family='Malgun Gothic')  # 윈도우 기본 한글 폰트
plt.rcParams['axes.unicode_minus'] = False

# null / not-null 개수 집계
counts = data['폐업일자'].isnull().value_counts()

# value_counts()는 {True: N1, False: N2} 형태이므로 라벨 지정
labels = ['폐업일자 없음(Null)', '폐업일자 있음(Not Null)']

# 순서 맞추기 위해 정렬
sizes = [counts.get(True, 0), counts.get(False, 0)]

# Pie Chart
plt.figure(figsize=(6, 6))
plt.pie(sizes, labels=labels, autopct=make_autopct_with_count)
plt.title('일반음식점 폐업일자 비율')
plt.savefig('./data_analysis/일반음식점폐업_파이차트.png', dpi=300, bbox_inches='tight')
plt.show()
data.set_index('사업장명')
columns = ['번호','개방서비스명','개방서비스아이디', '개방자치단체코드']
null_cols = data.columns[data.isnull().all()]
null_columns = list(null_cols)
data.drop(columns = null_columns,inplace = True)
data.set_index('사업장명',inplace = True)

print(data.info())