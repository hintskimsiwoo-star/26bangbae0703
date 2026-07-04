import streamlit as st
import pandas as pd

st.set_page_config(page_title="선생님 소개 - 방배중학교", page_icon="👩‍🏫")

st.title("👩‍🏫 선생님 소개")
st.write("방배중학교를 이끌어주시는 선생님들을 소개합니다.")

# 학년 선택 바
grade = st.selectbox("조회할 학년을 선택하세요", ["1학년", "2학년", "3학년"])

# 데이터 예시 (실제 정보에 맞게 수정 가능)
if grade == "2학년":
    st.subheader("📚 2학년 담당 선생님 목록")
    
    teacher_data = [
        {"역할/과목": "2학년 1반 담임 (수학)", "성함": "홍길동 선생님", "비고": "반갑습니다!"},
        {"역할/과목": "2학년 2반 담임 (영어)", "성함": "김철수 선생님", "비고": "Always do your best"},
        {"역할/과목": "역사 (교과 담당)", "성함": "이영희 선생님", "비고": "역사를 잊은 민족에게 미래는 없다"},
        {"역할/과목": "과학 (교과 담당)", "성함": "박민수 선생님", "비고": "실험실 안전 주의!"},
    ]
    
    df = pd.DataFrame(teacher_data)
    # 깔끔한 표로 출력
    st.table(df)
else:
    st.info(f"현재 {grade} 선생님 정보는 준비 중입니다. 코드를 수정해 데이터를 채워보세요!")
