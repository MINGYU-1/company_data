import os
import pandas as pd
base_dir = os.getcwd()
file_path = os.path.join(base_dir,'data_csv', '강원특별자치도_통신판매업.csv')
if not os.path.exists(file_path):
    print("경로에 파일이 존재하지 않습니다. 폴더 이름이나 파일명이 정확한지 확인하세요.")
else:
    try:
        data = pd.read_csv(file_path,encoding = 'cp949', low_memory= False)
        data_columns = list(data.columns)
        print('encoding제대로 하였습니다.')
    except UnicodeDecodeError:
        print("\n⚠️ CP949 인코딩 오류 발생! UTF-8로 다시 시도합니다.")
        data = pd.read_csv(file_path, encoding='utf-8', low_memory=False)
        data_columns = list(data.columns)
## 1. 컬럼들에 대해 조사하기
## 데이터 info보면 컬럼수 총 32개
data.info()
## 2. 데이터가 null인거 찾기 -> 그리고 다 지우기
null_cols = data.columns[data.isnull().all()]
data.drop(columns = null_cols,inplace = True)
data.info()
data['폐업일자'].isnull().size
import matplotlib.pyplot as plt
import pandas
plt.rc('font',family = 'Malgun Gothic')
plt.rcParams['axes.unicode_minus'] = False
import os

import numpy as np
total_size = data['폐업일자'].size
total_size
def make_autopct_with_count(pct):
    absolute_count = int(np.round(pct*total_size/100))
    return f"{pct:.1f}%\n({absolute_count}명)"
counts = data['폐업일자'].isnull().value_counts()
labels = ['폐업일자 없음(NULL)','폐업일자 있음(NOT NULL)']
sizes = [counts.get(True,0),counts.get(False,0)]
data['폐업일자'].isnull().value_counts()
save_path = os.path.join(os.getcwd(),'data_analysis','통신판매업_폐업차트_png')
plt.figure(figsize = (6,6))
plt.pie(sizes, labels = labels, autopct = make_autopct_with_count)
plt.title('통신판매업_폐업비율')
plt.savefig(save_path,dpi=300,bbox_inches = 'tight')
data.drop(columns = '자본금',inplace = True)
data_columns = data.columns
data_columns