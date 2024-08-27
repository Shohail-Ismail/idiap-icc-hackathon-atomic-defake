#!/usr/bin/env python
#
# Brief description here
#
##############################################################################
# Authors:
# - Alessio Xompero, alessio.xompero@gmail.com
#
#  Created Date: 2024/08/23
# Modified Date: 2023/08/26
#
# Copyright (c) 2024 AtomicDeFake
#
##############################################################################
import copy
import time
import uuid

import streamlit as st


contributor_qas = {
    "qa_pair": [
        {
            "question": "Is this OK? 1",
            "response_human": None,
        },
        {
            "question": "Is this OK? 2",
            "response_human": None,
        },
        {
            "question": "Is this OK? 3",
            "response_human": None,
        },
        {
            "question": "Is this OK? 4",
            "response_human": None,
        },
        {
            "question": "Is this OK? 5",
            "response_human": None,
        },
    ],
    "overall_label": None,
    "overall_certainty": None,
}


def send_answers_to_adf():
    my_qas = contributor_qas.copy()

    for idx in range(0, len(my_qas["qa_pair"])):
        my_qas["qa_pair"][idx]["question"] = (
            st.session_state.atomic_defake.generated_questions[idx]
        )
        my_qas["qa_pair"][idx]["response_human"] = st.session_state[
            "answer{:d}".format(idx)
        ]

    my_qas["overall_label"] = copy.copy(st.session_state.radio_trust)
    my_qas["overall_certainty"] = copy.copy(st.session_state.contributor_conf)

    ### Send the info to the backend
    st.session_state["contributor_qas"] = my_qas
    st.session_state.atomic_defake.set_human_responses(user_id, my_qas.copy())

    if st.session_state.n_checkers_iter == 0:
        st.session_state.stage = "adf_aggregation"
    else:
        print("switch_page")
        st.session_state.stage = "new_checker"


def questions_form():
    if st.session_state.atomic_defake.generated_questions is None:

        questions, _ = st.session_state.atomic_defake.generate_atomic_questions(
            st.session_state.post
        )
        st.session_state.atomic_defake.generated_questions = questions.copy()

    adf_questions = {
        "qa_pair": [
            {"question": q, "response_human": None}
            for q in st.session_state.atomic_defake.generated_questions
        ]
    }

    ## DEBUG DOES NOT WORK
    # adf_questions = st.session_state.atomic_defake.get_ai_questions_fake()

    # questions = [adf_questions["qa_pair"][x]["question"] for x in range(0,len(adf_questions["qa_pair"]))]
    # st.session_state.atomic_defake.generated_questions = questions.copy()
    ####

    st.divider()

    with st.form(key="questions_form", clear_on_submit=True):

        for idx in range(len(adf_questions["qa_pair"])):
            st.subheader("Question {:d}".format(idx + 1))
            st.text_area(
                adf_questions["qa_pair"][idx]["question"],
                value="",
                height=None,
                max_chars=500,
                key="answer{:d}".format(idx),
                help=None,
                on_change=None,
                args=None,
                label_visibility="visible",
            )

        st.radio(
            "Given the questions and the answers you found, how would you rate the post trustworthiness?",
            key="radio_trust",
            options=[
                "Trustworthy",
                "Somewhat trustworthy",
                "I don't know",
                "Not trustworthy",
            ],
        )

        st.select_slider(
            "How confident are you in your answers?",
            key="contributor_conf",
            options=[
                "very uncertain",
                "uncertain",
                "neither certain nor uncertain",
                "certain",
                "very certain",
            ],
        )

        submit_button = st.form_submit_button(
            label="Submit",
            on_click=send_answers_to_adf,
        )


############################################################################

user_id = str(uuid.uuid1())

st.title("AtomicDeFake")
st.header("Contributor {:s}".format(user_id))
st.divider()

print(st.session_state.stage)
print(st.session_state.post)
print(st.session_state.atomic_defake.generated_questions)


if st.session_state.stage == "contributor":
    st.text(
        """
        Please answer to the list of questions below
        to identify if any misleading information is present in the following post.
        """
    )

    if "post" in st.session_state:
        st.text(st.session_state.post)

    questions_form()

elif st.session_state.stage == "new_checker":
    print(st.session_state.n_checkers_iter)
    post_tmp = copy.copy(st.session_state.post)
    st.session_state.n_checkers_iter = st.session_state.n_checkers_iter - 1
    print(st.session_state.n_checkers_iter)

    st.session_state.stage = "contributor"
    st.session_state.post = post_tmp

    st.rerun()


elif st.session_state.stage == "adf_aggregation":
    time.sleep(3)
    # st.session_state.atomic_defake.detect_mislead_info_fake()
    st.session_state.atomic_defake.detect_mislead_info()

    if st.session_state.atomic_defake.get_status() == "completed":
        st.session_state.stage = "output"
        st.switch_page("user_post.py")

else:
    st.text(
        """
        There is no post for you to review.
        You will be notified when the post of another user is ready to be reviewed.
        """
    )
