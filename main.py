import streamlit as st
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="지구촌 MBTI 분석기", page_icon="🌍", layout="wide")

st.title("🌍 나라별 MBTI 순위 분석 대시보드")
st.markdown("국가별 MBTI 분포와 순위를 확인해보세요!")

# 2. CSV 데이터 로드 함수 (캐싱 처리로 속도 향상)
@st.cache_data
def load_data():
    # 제공해주신 파일명을 넣어 바로 읽어옵니다.
    # 인코딩 문제가 발생할 경우를 대비해 encoding='utf-8'을 추가했습니다.
    df = pd.read_csv('countriesMBTI_16types.csv', encoding='utf-8')
    return df

# 데이터 로드
try:
    df = load_data()
except FileNotFoundError:
    st.error("🚨 'countriesMBTI_16types.csv' 파일을 찾을 수 없습니다.")
    st.info("💡 팁: 깃허브 리포지토리에 `main.py`와 `countriesMBTI_16types.csv` 파일이 같은 폴더(루트)에 있는지 확인해주세요.")
    st.stop()
except Exception as e:
    st.error(f"데이터를 불러오는 중 오류가 발생했습니다: {e}")
    st.stop()

# --- 대시보드 기능 구현 ---

# 3. CSV 파일의 실제 컬럼명 탐색 및 매핑
# CSV 파일 구조에 맞춰 국가, MBTI, 수치 컬럼을 자동으로 잡거나 안내합니다.
columns = df.columns.tolist()

# 일반적으로 국가명 컬럼으로 쓰이는 이름들 체크 (없으면 첫 번째 컬럼 사용)
country_col = next((c for c in columns if c.lower() in ['country', '국가', 'nation']), columns[0])
# 일반적으로 MBTI 컬럼으로 쓰이는 이름들 체크 (없으면 두 번째 컬럼 사용)
mbti_col = next((c for c in columns if c.lower() in ['mbti', 'type']), columns[1] if len(columns) > 1 else columns[0])
# 일반적으로 수치(비율/개수) 컬럼으로 쓰이는 이름들 체크
val_col = next((c for c in columns if c.lower() in ['percentage', 'ratio', 'count', '비율', '수']), None)

# 만약 수치 컬럼을 못 찾았다면 숫자형 데이터 중 첫 번째 컬럼 선택
if not val_col:
    num_cols = df.select_dtypes(include=['number']).columns.tolist()
    val_col = num_cols[0] if num_cols else columns[-1]

# 국가 선택 박스 만들기
country_list = df[country_col].unique()
selected_country = st.selectbox("👉 분석할 국가를 선택하세요:", sorted(country_list))

if selected_country:
    # 선택된 국가의 데이터만 필터링
    country_df = df[df[country_col] == selected_country].copy()
    
    # 많은 순서대로 정렬 및 순위 매기기
    country_df = country_df.sort_values(by=val_col, ascending=False).reset_index(drop=True)
    country_df.index = country_df.index + 1  # 1등부터 시작
    country_df.index.name = '순위'
    
    # 화면 레이아웃 분할 (좌측: 차트, 우측: 표)
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader(f"📊 {selected_country}의 MBTI 분포 그래프")
        # 스트림릿 내장 바 차트로 시각화
        st.bar_chart(data=country_df, x=mbti_col, y=val_col, use_container_width=True)
        
    with col2:
        st.subheader(f"🥇 {selected_country} MBTI 순위 리스트")
        # 깔끔하게 순위가 매겨진 데이터프레임 출력
       country_df = country_df.loc[:, ~country_df.columns.duplicated()]

if mbti_col == val_col:
    st.dataframe(country_df[[mbti_col]], use_container_width=True)
else:
    st.dataframe(country_df[[mbti_col, val_col]], use_container_width=True)

    # 간단한 요약 정보
    top_mbti = country_df.iloc[0][mbti_col]
    st.success(f"💡 {selected_country}에서 가장 많은 비율을 차지하는 MBTI는 **{top_mbti}**입니다!")
    
