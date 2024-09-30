import os
from openai import OpenAI
import streamlit as st

# Set up OpenAI API key from Streamlit secrets
os.environ["OPENAI_API_KEY"] = st.secrets['API_KEY']
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

# Set up the Streamlit page
st.set_page_config(
    page_title="일타강사의 강의법",
    page_icon="👨‍🏫",
    layout="centered",
    initial_sidebar_state="auto",
)

# Custom CSS for a more professional UI
st.markdown("""
    <style>
        .main {
            background-color: #f0f2f6;
            font-family: 'Arial', sans-serif;
        }
        h1 {
            color: #2c3e50;
            text-align: center;
            font-family: 'Arial', sans-serif;
            font-size: 2.5em;
        }
        .instructions {
            background-color: #ecf0f1;
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 20px;
            box-shadow: 2px 2px 5px #bdc3c7;
        }
        .section {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 2px 2px 5px #bdc3c7;
            margin-bottom: 20px;
            font-size: 1em;
        }
        .button {
            background-color: #3498db;
            color: white;
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
            border-radius: 5px;
            border: none;
            cursor: pointer;
            width: 100%;
        }
        .button:hover {
            background-color: #2980b9;
        }
    </style>
""", unsafe_allow_html=True)

# Title of the application
st.markdown("<h1>일타강사의 강의법 👨‍🏫</h1>", unsafe_allow_html=True)

# Instructions for users
st.markdown("""
<div class="instructions">
    <h3>사용 방법</h3>
    <ul>
        <li><strong>강의 주제</strong>: 강의할 주제나 내용을 입력하세요.</li>
        <li><strong>대상 학습자</strong>: 강의 대상이 되는 학습자의 특성을 입력하세요.</li>
        <li><strong>강의 방식</strong>: 원하는 강의 방식을 선택하세요.</li>
        <li><strong>추가 요구사항</strong>: 강의에 대한 추가적인 요구사항이나 고려사항을 입력하세요.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# User inputs
st.markdown("<div class='section'>", unsafe_allow_html=True)

topic = st.text_area("강의 주제 입력 📚", height=100, placeholder="강의할 주제나 내용을 입력하세요. 예: '지구 온난화의 원인과 영향'")

audience = st.text_input("대상 학습자 💡", placeholder="강의 대상이 되는 학습자의 특성을 입력하세요. 예: '고등학교 2학년 과학 수업'")

teaching_methods = ["강의식", "토론식", "프로젝트 기반", "문제 중심 학습", "플립 러닝", "게이미피케이션", "협동 학습"]
selected_method = st.selectbox("강의 방식 선택", teaching_methods)

additional_requirements = st.text_area("추가 요구사항 (선택사항) 🔍", height=100, placeholder="강의에 대한 추가적인 요구사항이나 고려사항을 입력하세요. 예: '15분 분량의 짧은 강의로 구성', '시각적 자료 활용 필요'")

st.markdown("</div>", unsafe_allow_html=True)

# Button to generate the lecture method
if st.button('강의법 생성하기', key='generate_button', help="선택한 조건에 맞는 강의법을 생성합니다"):
    with st.spinner('생성 중입니다...'):
        # Combine inputs into a single prompt
        prompt = f"""
        강의 주제: {topic}
        대상 학습자: {audience}
        강의 방식: {selected_method}
        추가 요구사항: {additional_requirements}
        """
        
        # Create a chat completion request to OpenAI API
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                },
                {
                    "role": "system",
                    "content": 
                        "당신은 창의적이고 효과적인 강의법 전문가입니다. 주어진 정보를 바탕으로 최적의 강의 방법을 제안해주세요."
                        "1. 강의 주제와 대상 학습자의 특성을 고려하여 적절한 난이도와 접근 방식을 선택하세요."
                        "2. 선택된 강의 방식에 맞는 구체적인 강의 전략과 활동을 제안하세요."
                        "3. 학습자의 참여와 이해를 높일 수 있는 창의적인 아이디어를 포함하세요."
                        "4. 추가 요구사항을 반영하여 강의 계획을 조정하세요."
                        "5. 강의의 도입, 전개, 정리 단계별로 구체적인 활동과 시간 배분을 제시하세요."
                        "6. 필요한 교구나 자료, 기술적 요구사항이 있다면 명시하세요."
                        "7. 학습 목표 달성을 위한 평가 방법도 제안해주세요."
                        "8. 마지막으로, 이 강의법을 효과적으로 실행하기 위한 팁을 2-3가지 제공해주세요."
                }
            ],
            model="gpt-4o",
        )

        # Extract the generated content
        result = chat_completion.choices[0].message.content

        # Display the result in Streamlit app
        st.markdown("<div class='section'>", unsafe_allow_html=True)
        st.write("### 생성된 강의법:")
        st.write(result)
        st.markdown("</div>", unsafe_allow_html=True)