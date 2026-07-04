import streamlit as st
import pandas as pd

st.set_page_config(page_title="학사일정 - 방배중학교", page_icon="📅")

st.title("📅 학사일정")
st.write("방배중학교의 주요 학사일정입니다. 시험 및 방학 기간을 확인하세요.")

# 학사일정 데이터 구성
schedule_data = {
    "월별": ["3월", "4월", "5월", "6월", "7월", "8월"],
    "주요 행사 및 시험 일정": [
        "입학식 및 개학식, 학급 임원 선거",
        "지필평가(중간고사), 과학의 달 행사",
        "체육대회, 현장체험학습(소풍)",
        "수행평가 집중 기간",
        "지필평가(기말고사), 여름방학식",
        "2학기 개학식"
    ]
}

df_schedule = pd.DataFrame(schedule_data).set_index("월별")

# 데이터 프레임 출력
st.dataframe(df_schedule, use_container_width=True)

st.markdown("---")
st.warning("💡 **주의사항:** 상세 일정은 학교 사정에 따라 변경될 수 있으니 가정통신문을 반드시 확인하세요.")
