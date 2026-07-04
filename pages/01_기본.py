import streamlit as st

st.set_page_config(page_title="학교소개 - 방배중학교", page_icon="🏫")

st.title("🏫 방배중학교 소개")
st.write("방배중학교의 자랑스러운 상징과 교가를 소개합니다.")

# 탭 구성
tab1, tab2 = st.tabs(["✨ 교훈 및 상징", "🎶 교가"])

with tab1:
    st.subheader("🎯 교훈")
    st.success("**바르고 슬기 우람하게**")
    
    st.markdown("---")
    st.subheader("🌿 학교 상징")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="교목 (학교 나무)", value="은행나무")
        st.write("의지, 번영, 사회에 쓸모 있는 사람을 상징합니다.")
    with col2:
        st.metric(label="교화 (학교 꽃)", value="장미")
        st.write("사랑, 열정, 아름다운 마음씨를 상징합니다.")

