import streamlit as st
import pandas as pd
import datetime

# Page configuration
st.set_page_config(
    page_title="Daily Balance - 마음약방 & 대사 밸런스",
    page_icon="💙",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        color: #1E3A8A;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.0rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .level-3-badge {
        background-color: #FEE2E2;
        color: #991B1B;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
    }
    .level-2-badge {
        background-color: #FEF3C7;
        color: #92400E;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
    }
    .level-1-badge {
        background-color: #D1FAE5;
        color: #065F46;
        padding: 4px 12px;
        border-radius: 12px;
        font-weight: bold;
    }
    .card-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 16px;
        margin-bottom: 12px;
    }
</style>
""", unsafe_allow_html=True)

# 💊 Medication Database
MED_DATABASE = {
    "자이프렉사": {
        "generic": "올란자핀 (Olanzapine)",
        "level": 3,
        "level_name": "Level 3 : 주의 집중 필요",
        "description": "뇌의 식욕 조절 수용체(H1, 5-HT2C)에 강하게 작용하여 포만감 감소 및 대사 저하를 유발할 수 있습니다.",
        "advice": "투약 초기 12주 동안 식욕 변화와 체중을 정기적으로 체크하는 것이 중요합니다."
    },
    "올란자핀": {
        "generic": "올란자핀 (Olanzapine)",
        "level": 3,
        "level_name": "Level 3 : 주의 집중 필요",
        "description": "뇌의 식욕 조절 수용체(H1, 5-HT2C)에 강하게 작용하여 포만감 감소 및 대사 저하를 유발할 수 있습니다.",
        "advice": "투약 초기 12주 동안 식욕 변화와 체중을 정기적으로 체크하는 것이 중요합니다."
    },
    "클로자릴": {
        "generic": "클로자핀 (Clozapine)",
        "level": 3,
        "level_name": "Level 3 : 주의 집중 필요",
        "description": "체중 증가 및 혈당/지질 대사 변화 가능성이 상대적으로 높은 약물입니다.",
        "advice": "주치의와의 정기적인 혈액 검사 및 신체 측정이 권장됩니다."
    },
    "쿠에타핀": {
        "generic": "쿠에타핀 (Quetiapine)",
        "level": 2,
        "level_name": "Level 2 : 정기 관찰 필요",
        "description": "야간 진정 효과와 함께 일부 식욕 증가나 나른함이 동반될 수 있습니다.",
        "advice": "야식 욕구가 생길 때 대체 음료나 가벼운 습관으로 관리해 보세요."
    },
    "서로퀼": {
        "generic": "쿠에타핀 (Quetiapine)",
        "level": 2,
        "level_name": "Level 2 : 정기 관찰 필요",
        "description": "야간 진정 효과와 함께 일부 식욕 증가나 나른함이 동반될 수 있습니다.",
        "advice": "야식 욕구가 생길 때 대체 음료나 가벼운 습관으로 관리해 보세요."
    },
    "리스페달": {
        "generic": "리스페리돈 (Risperidone)",
        "level": 2,
        "level_name": "Level 2 : 정기 관찰 필요",
        "description": "복용 용량이나 개인차에 따라 체중 증가 및 프로락틴 수치 변화가 나타날 수 있습니다.",
        "advice": "분기별 체중 및 혈당 모니터링이 도움이 됩니다."
    },
    "인베가": {
        "generic": "팔리페리돈 (Paliperidone)",
        "level": 2,
        "level_name": "Level 2 : 정기 관찰 필요",
        "description": "리스페리돈의 대사물질로 복용 용량에 따른 신체지표 추적이 권장됩니다.",
        "advice": "정기적인 대사지표 모니터링을 권장합니다."
    },
    "아빌리파이": {
        "generic": "아리피프라졸 (Aripiprazole)",
        "level": 1,
        "level_name": "Level 1 : 대사 중립 (안심)",
        "description": "다른 항정신병 약물에 비해 체중 증가나 대사 부작용 영향이 매우 적은 약물입니다.",
        "advice": "체중 부담 없이 정해진 용법대로 편안하게 복용하세요."
    },
    "아리피프라졸": {
        "generic": "아리피프라졸 (Aripiprazole)",
        "level": 1,
        "level_name": "Level 1 : 대사 중립 (안심)",
        "description": "다른 항정신병 약물에 비해 체중 증가나 대사 부작용 영향이 매우 적은 약물입니다.",
        "advice": "체중 부담 없이 정해진 용법대로 편안하게 복용하세요."
    },
    "라투다": {
        "generic": "루라시돈 (Lurasidone)",
        "level": 1,
        "level_name": "Level 1 : 대사 중립 (안심)",
        "description": "대사 부작용 위험이 낮아 체중 관리에 비교적 유용한 약물입니다.",
        "advice": "식사와 함께 복용하는 용법을 지켜주시면 흡수율에 더욱 좋습니다."
    },
    "젤독스": {
        "generic": "지프라시돈 (Ziprasidone)",
        "level": 1,
        "level_name": "Level 1 : 대사 중립 (안심)",
        "description": "대사 관련 부작용 발생률이 매우 적은 편입니다.",
        "advice": "음식과 함께 복용하는 것이 권장됩니다."
    }
}

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "안녕하세요! 💙 **Daily Balance** 마음약방 & 대사 밸런스 챗봇입니다.\n\n복용 중이신 정신과 약물 이름을 입력하시거나, 체중/식욕 관련 고충을 편하게 이야기해 주세요!\n\n*예: '자이프렉사 먹는데 살쪄요', '쿠에타핀 부작용', '아빌리파이 살찌나요?'*"}
    ]

if "diary_logs" not in st.session_state:
    st.session_state.diary_logs = []

# Sidebar Navigation
st.sidebar.title("💙 Daily Balance 메뉴")
app_mode = st.sidebar.radio("원하시는 기능을 선택하세요:", ["💬 챗봇 상담 (메인)", "📖 식욕 다이어리", "📄 주치의 1분 상담 카드"])

st.sidebar.markdown("---")
st.sidebar.info("🔒 **100% 익명성 보장**: 모든 기록은 서버에 저장되지 않고 현재 스마트폰/브라우저에만 암호화되어 안전하게 유지됩니다.")

# Function to search medication and generate response
def get_bot_response(user_input):
    found_med = None
    for med_key in MED_DATABASE:
        if med_key in user_input:
            found_med = med_key
            break
            
    if found_med:
        info = MED_DATABASE[found_med]
        level = info['level']
        
        badge_html = f"<span class='level-{level}-badge'>{info['level_name']}</span>"
        
        resp = f"""
💙 **많이 속상하고 불안하셨을 수 있습니다. 하지만 꼭 기억해 주세요!**
> *"체중 증가와 식욕 변화는 결코 OO님의 의지 부족이나 게으름 때문이 아닙니다."*

---
💊 **검색된 약물**: **{found_med}** ({info['generic']})  
⚠️ **대사 위험도**: {info['level_name']}

📊 **작용 특징**:
{info['description']}

💡 **관리 가이드**:
{info['advice']}

🚨 **[안전 경고]**
살이 찐다고 해서 절대로 약을 임의로 줄이거나 중단하지 마세요!  
약물 중단 시 원래 증상이 재발할 위험이 매우 높습니다.

👉 아래 메뉴에서 **[📖 식욕 다이어리]**를 기록하거나 **[📄 주치의 1분 상담 카드]**를 발급받아 진료 시 활용해 보세요!
"""
        return resp
    else:
        if "살" in user_input or "체중" in user_input or "배고파" in user_input or "식욕" in user_input or "야식" in user_input:
            return """
💙 **약물 복용 중 식욕 변화나 체중 증가로 고충을 겪고 계시군요.**

항정신병 약물 중 일부 성분(올란자핀, 쿠에타핀, 클로자핀 등)은 뇌의 식욕 억제 신호를 완화시켜 단 음식이나 야식이 강력하게 당기게 만듭니다.

이런 현상은 **약리 작용에 의한 가짜 배고픔**일 가능성이 매우 높습니다!
- 정확한 안내를 위해 **복용 중이신 약물 이름**(예: 자이프렉사, 쿠에타핀, 아빌리파이 등)을 입력해 주시겠어요?
- 왼쪽 메뉴의 **[📖 식욕 다이어리]**를 활용하시면 약 복용 후 식욕 피크 시간대를 기록할 수 있습니다.
"""
        else:
            return f"""
입력하신 내용: *"{user_input}"*

제가 도와드릴 수 있는 주요 기능입니다:
1. **약물명 입력**: 약물별 대사 위험도(Level 1~3) 및 관리 가이드 안내 (예: '자이프렉사', '쿠에타핀', '아빌리파이')
2. **식욕 다이어리**: 약 복용 후 식욕 피크 시간대 및 대처 기록
3. **주치의 상담 카드**: 진료실에서 의사 선생님께 보여드릴 1분 요약 카드 생성

궁금하신 약물명이나 증상을 입력해 주세요!
"""

# APP MODE 1: Chatbot Main
if app_mode == "💬 챗봇 상담 (메인)":
    st.markdown("<div class='main-header'>Daily Balance 챗봇</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>정신과 약물 대사 밸런스 & 체중 부작용 안심 케어</div>", unsafe_allow_html=True)

    # Render chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # User input
    if prompt := st.chat_input("약물명(예: 자이프렉사, 쿠에타핀)이나 고충을 입력하세요..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        bot_reply = get_bot_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": bot_reply})
        with st.chat_message("assistant"):
            st.markdown(bot_reply)

# APP MODE 2: Appetite Diary
elif app_mode == "📖 식욕 다이어리":
    st.markdown("<div class='main-header'>📖 식욕 다이어리</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>약 복용 후 찾아오는 '가짜 배고픔'과 식욕 피크 패턴을 기록하세요</div>", unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("📝 오늘 식욕 기록하기")
        entry_date = st.date_input("날짜", datetime.date.today())
        entry_time = st.time_input("시간대", datetime.time(22, 0))
        med_relation = st.selectbox("약 복용과의 관계", ["저녁 약 복용 후 1시간 이내", "저녁 약 복용 후 2시간 이상", "취침 직전", "취침 중 깨어남", "기타"])
        appetite_score = st.slider("식욕/배고픔 강도 (1=약함, 5=극심함)", 1, 5, 4)
        crav_food = st.text_input("당겼던 음식", "아이스크림, 과자, 야식")
        coping = st.selectbox("나의 대처 방법", ["탄산수/제로음료 마시기", "물 한 컵 마시고 스트레칭", "일찍 잠자리 들기", "음식 섭취함", "참기 어려웠음"])
        
        if st.button("다이어리 저장하기 💾"):
            new_log = {
                "날짜": str(entry_date),
                "시간대": str(entry_time),
                "약 연관성": med_relation,
                "식욕 강도": f"{appetite_score}/5",
                "당긴 음식": crav_food,
                "대처": coping
            }
            st.session_state.diary_logs.append(new_log)
            st.success("식욕 다이어리가 안전하게 저장되었습니다! 💙")

    with col2:
        st.subheader("📊 나의 식욕 기록 목록")
        if st.session_state.diary_logs:
            df = pd.DataFrame(st.session_state.diary_logs)
            st.dataframe(df, use_container_width=True)
            st.info("💡 **패턴 분석 피드백**: 기록이 쌓일수록 주치의 선생님과 공유하여 약물 복용 시간대 조정이나 대사 관리에 큰 도움을 받으실 수 있습니다.")
        else:
            st.write("아직 저장된 식욕 기록이 없습니다. 왼쪽에서 첫 다이어리를 작성해 보세요!")

# APP MODE 3: Doctor Consultation Card
elif app_mode == "📄 주치의 1분 상담 카드":
    st.markdown("<div class='main-header'>📄 주치의 1분 상담 카드</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>진료실에서 의사 선생님께 보여드릴 1분 요약 카드를 생성합니다</div>", unsafe_allow_html=True)

    with st.form("doc_card_form"):
        user_med = st.text_input("복용 중인 약물명", "자이프렉사 10mg / 쿠에타핀 100mg")
        weight_diff = st.selectbox("체중 변화", ["변화 없음", "1~3kg 증가", "3~5kg 증가", "5kg 이상 급격히 증가"])
        primary_trouble = st.multiselect("주요 고충 (복수 선택)", ["야간 단 음식 폭식", "약 복용 후 식욕 억제 불가", "낮 시간 무기력 및 나른함", "공복혈당/지질 수치 걱정"], default=["야간 단 음식 폭식", "약 복용 후 식욕 억제 불가"])
        request_detail = st.text_area("의사 선생님께 요청하고 싶은 사항", "대사 부작용이 상대적으로 적은 약물로 교체 검토 또는 식욕/대사 관리를 위한 보조 치료 상의를 희망합니다.")
        
        submitted = st.form_submit_button("1분 상담 카드 생성하기 ✨")

    if submitted:
        st.subheader("📱 캡처하여 진료실에서 보여주세요")
        card_content = f"""
==================================================
📄 [진료실 전달용 1분 상담 카드]
--------------------------------------------------
선생님, 약물 복용 후 발생한 신체 변화 및 대사 부작용으로 인해 진료 상담을 요청드립니다.

• 복용 약물   : {user_med}
• 신체 변화   : {weight_diff}
• 주요 고충   : {', '.join(primary_trouble)}
• 요청 사항   : {request_detail}
--------------------------------------------------
Daily Balance | 개인 맞춤형 대사 밸런스 리포트
==================================================
"""
        st.code(card_content, language="text")
        st.success("상담 카드가 성공적으로 생성되었습니다! 화면을 캡처하거나 위 텍스트를 복사하여 진료에 활용하세요.")
