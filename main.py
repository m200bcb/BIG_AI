import openai
import streamlit as st
from streamlit_option_menu import option_menu
import create_contents as cc
from connect import session
from models.tables import Problem, WA, Dates
from datetime import datetime

#streamlit run main.py
options = ['1. print', '2. 자료형', '3. if문', '4. while문', '5. for문', '6. 함수', '7. 클래스',
           '8. 그리디 알고리즘', '9. 다이나믹 프로그래밍', '복습']
messages = []

with st.sidebar:
    menu = option_menu(
        menu_title='Python',
        options=options,
        menu_icon='playstation',
        styles={
            'container': {'padding': '5!important', 'background-color': 'teal'},
            'icon': {'color': 'white', 'font-size': '18px'},
            'nav-link': {'color': 'white', 'font-size': '18px',
                         'text-align': 'left', 'margin': '0px',
                         '--hover-color': 'cornflowerblue'},
            'nav-link-selected': {'background-color': '	dodgerblue'}
        },
    )

i = options.index(menu)
if i != len(options) - 1:
    problem_idx = int(1)
    st.subheader(str(options[i]))

    filtered_problem = (
        Problem.query.filter_by(pb_no=i+1).all()
    )

    if filtered_problem:
        messages.append({"role":"assistant", "content":str(problem_idx)+'번 문제는 '+str(filtered_problem)})
        result = {"result": filtered_problem[0].pb_questions}
        st.write(filtered_problem[0].pb_questions)

    else:
        query = f"{options[i]}에 대한 설명과 그에 관한 실습 과제 문제를 1개 만들어줘. 문제는 요구 명세가 주어졌을 때 소스코드를 짜는 형태야. 정답 소스코드도 알려주는데 형식은 '정답 소스코드:' 뒤에 출력해줘."
        result = cc.qa({"query": query})

        messages.append({"role":"assistant", "content":str(problem_idx)+'번 문제는 '+str(result["result"])})
        st.write(result["result"].split('정답 소스코드:')[0], str(result["source_documents"][0].metadata))

        problem = Problem(
            pb_questions=result["result"].split('정답 소스코드:')[0],
            pb_answers=result["result"].split('정답 소스코드:')[1],
            pb_no=i+1
        )

        session.add(problem)
        session.commit()

    with st.form("정답 코드 입력"):
        message = st.text_area('정답 코드를 입력하세요(에디터에서 입력후 붙여넣으세요)', height=30)
        submit_button1 = st.form_submit_button('제출')

        if submit_button1:
            messages.append({"role":"user", "content":message+f"{problem_idx}번 문제에 대한 정답이 이게 맞아?"})

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.1
            )

            chat_response = completion.choices[0].message.content
            if not '정답입' in chat_response:
                today = str(datetime.now().date())
                new_d = Dates(
                    dates = today,
                )

                new_d.wrong_answers = WA(date=today, wrong_answers=message, wrong_reasons=chat_response)
                new_d.problems = Problem(pb_questions=result["result"].split('정답 소스코드:')[0], pb_no=i+1)

                session.add(new_d)
                session.commit()

            st.write(f'{chat_response}')
            messages.append({"role":"assistant", "content":chat_response})

    placeholder = st.empty()
    with placeholder.expander("Answer:", expanded=False):
        if filtered_problem:
            st.write(filtered_problem[0].pb_answers)
        else:
            st.write(result["result"].split('정답 소스코드:')[1], str(result["source_documents"][0].metadata))

    with st.form("추가 문제 생성"):
        button1 = st.form_submit_button('유사문제')

        if button1:
            problem_idx += 1
            placeholder.empty()
            messages.append({"role": "user", "content": message + f"{options[i].split('.')[1]}를 사용한 다른 문제를 하나 생성해줘."})

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.7
            )

            chat_response = completion.choices[0].message.content
            st.write(f'{chat_response}')
            messages.append({"role": "assistant", "content": str(problem_idx)+chat_response})

            messages.append({"role": "user", "content": message + f"{problem_idx}번 문제에 대한 예시답안을 알려줘."})

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=0.1
            )

            chat_response = completion.choices[0].message.content
            answer_code = f'{chat_response}'
            with placeholder.expander("Answer:", expanded=False):
                st.write(answer_code)
            messages.append({"role": "assistant", "content": chat_response})



elif i == 9:
    st.subheader('복습')

    col1, col2 = st.columns((1, 3))
    filtered = (
        session.query(Dates)
        .all()
    )

    l = [filtered[0].dates]
    date_selected = col1.selectbox('날짜 선택:', l)
    ans = filtered[0].wrong_answers
    past_reasons = filtered[0].wrong_reasons

    st.write(ans)
    st.write('\n')
    st.write('당신이 과거에 잘못 작성한 코드입니다. 틀린 이유를 말해보세요.')
    st.text_area('이유 입력', height=20)
    with st.expander("정답"):
        st.write('정답')
        st.write(past_reasons)

