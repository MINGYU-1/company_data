# app.py
import mysql.connector
import os
import json
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template

# 환경 설정
load_dotenv()
db_password = os.getenv('password')

app = Flask(__name__, template_folder='.') # 현재 디렉터리를 템플릿 폴더로 사용
app.config['JSON_AS_ASCII'] = False # 한글 깨짐 방지

# --- DB 연결 및 데이터 로드 함수 (Streamlit 코드 재사용) ---
def get_db_connection():
    try:
        conn = mysql.connector.connect(
            host="127.0.0.1",
            user="root",
            password=db_password,
            database="new_schema"
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Database Connection Error: {err}")
        return None

def load_data_to_df(conn, table_name, query):
    try:
        final_query = query.format(table_name=table_name)
        df = pd.read_sql(final_query, conn)
        return df
    except Exception as e:
        print(f"테이블 '{table_name}' 로드 실패: {e}")
        return pd.DataFrame()

def prepare_ui_data():
    conn = get_db_connection()
    if not conn:
        return {}

    # a) 사업체 위치 데이터 (지도 활용)
    df_biz_coords = load_data_to_df(conn, 'chuncheon_businesses_with_coords',
                                    query="SELECT 업종, 업소명, 위도, 경도 FROM {table_name}")
    # b) 강원도 사업체 상세 목록 (비교 및 목록용)
    df_kangwon = load_data_to_df(conn, 'kangwondo_businesses',
                                 query="SELECT 업종, 업소명, 주소, 연락처 FROM {table_name}")
    
    conn.close()

    # --- 데이터 정리 및 컬럼명 통일 ---
    if not df_biz_coords.empty:
        df_biz_coords.columns = ['type', 'name', 'lat', 'lon']
        df_biz_coords = df_biz_coords.dropna(subset=['lat', 'lon'])
    
    if not df_kangwon.empty:
        df_kangwon.columns = ['type', 'name', 'address', 'contact']
        df_kangwon['region'] = df_kangwon['address'].apply(lambda x: '춘천시' if '춘천시' in str(x) else '강원도 타 지역')

    return df_biz_coords, df_kangwon

# --- Flask 라우트 정의 ---

@app.route('/')
def index():
    """메인 HTML 템플릿 로드"""
    return render_template('index.html')

@app.route('/api/businesses')
def api_businesses():
    """사업체 위치 및 상세 정보 API"""
    df_biz_coords, df_kangwon = prepare_ui_data()

    # 지도용 데이터 (리스트 형태로 변환)
    map_data = df_biz_coords.to_dict('records')

    # 비교 및 목록용 데이터 (업종별 카운트를 JSON으로)
    biz_counts = df_kangwon.groupby(['region', 'type']).size().reset_index(name='count')
    
    # 상세 목록 데이터 (리스트 형태로 변환)
    list_data = df_kangwon.to_dict('records')

    return jsonify({
        'map_data': map_data,
        'chart_data': biz_counts.to_dict('records'),
        'list_data': list_data
    })

if __name__ == '__main__':
    # Flask 실행 전 DB 연결 테스트
    if get_db_connection():
        print("Flask 서버 시작...")
        app.run(debug=True)