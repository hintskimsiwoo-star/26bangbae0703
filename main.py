import streamlit as tf
import pandas as pd
import sqlite3

# 1. 페이지 설정
st.set_page_config(page_title="지구촌 MBTI 분석기", page_icon="🌍", layout="wide")

st.title("🌍 나라별 MBTI 순위 분석 대시보드")
st.markdown("데이터베이스에 저장된 국가별 MBTI 분포와 순위를 확인해보세요!")

# 2. 데이터베이스 연결 함수 (캐싱 처리로 속도 향상)
@st.cache_data
def load_data():
    # 'mbti_data.db' 자리에 실제 첨부하신 db 파일명을 적어주세요.
    conn = sqlite3.connect('mbti_data.db')
    
    # 예시 테이블명 'country_mbti' (실제 테이블명으로 수정 필요)
    # 테이블 구조 예시: [Country, MBTI, Percentage(또는 Count)]
    query = "SELECT * FROM country_mbti"
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# 데이터 로드
try:
    df = load_data()
except Exception as e:
    st.error("데이터베이스를 불러오는 데 실패했습니다. 파일명과 테이블명을 확인해주세요.")
    st.info("💡 팁: 테이블 구조가 [국가, MBTI, 비율] 형태로 되어 있어야 작동합니다.")
    st.stop()

# --- 대시보드 기능 구현 ---

# 국가 선택 박스 만들기
country_list = df['Country'].unique()
selected_country = st.selectbox("👉 분석할 국가를 선택하세요:", sorted(country_list))

if selected_country:
    # 선택된 국가의 데이터만 필터링
    country_df = df[df['Country'] == selected_country].copy()
    
    # 많은 순서대로 정렬 (열 이름이 Percentage 또는 Count라고 가정)
    # 데이터베이스 컬럼명에 맞게 'Percentage' 부분을 수정하세요.
    if 'Percentage' in country_df.columns:
        val_col = 'Percentage'
    elif 'Count' in country_df.columns:
        val_col = 'Count'
    else:
        # 데이터베이스의 수치 데이터 컬럼명을 자동으로 탐색
        val_col = country_df.select_dtypes(include=['number']).columns[0]

    # 높은 순 정렬 및 순위 매기기
    country_df = country_df.sort_values(by=val_col, ascending=False).reset_index(drop=True)
    country_df.index = country_df.index + 1  # 인덱스를 1등부터 시작하도록 수정
    country_df.index.name = '순위'
    
    # 화면 레이아웃 분할 (좌측: 차트, 우측: 표)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📊 {selected_country}의 MBTI 분포 그래프")
        # 스트림릿 내장 바 차트로 시각화
        st.bar_chart(data=country_df, x='MBTI', y=val_col, use_container_width=True)
        
    with col2:
        st.subheader(f"🥇 {selected_country} MBTI 순위 리스트")
        # 깔끔하게 순위가 매겨진 데이터프레임 출력
        st.dataframe(country_df[['MBTI', val_col]], use_container_width=True)

    # 간단한 요약 정보
    top_mbti = country_df.iloc[0]['MBTI']
    st.success(f"💡 {selected_country}에서 가장 많은 비율을 차지하는 MBTI는 **{top_mbti}**입니다!")
