import streamlit as st


contributor_qas = {
    "qa_pair" : [
    {
        "question": "Is this OK? 1",
        "response_human" : None,
    },
    {
        "question": "Is this OK? 2",
        "response_human" : None,
    },
    {
        "question": "Is this OK? 3",
        "response_human" : None,
    },
    {
        "question": "Is this OK? 4",
        "response_human" : None,
    },
    {
        "question": "Is this OK? 5",
        "response_human" : None,
    },
    ],
    "overall_label" : None,
    "overall_certainty" : None,
}


def send_answers_to_adf():
    """
    """
    my_qas = contributor_qas.copy()

    for idx in range(0,5):
        my_qas["qa_pair"][idx]["response_human"] = st.session_state["answer{:d}".format(idx)]
    
    my_qas["overall_label"] = st.session_state.radio_trust
    my_qas["overall_certainty"] = st.session_state.contributor_conf

    st.session_state.atomic_defake.get_ai_questions_fake()



    st.session_state["contributor_qas"] = my_qas
    st.session_state.stage = ""


def questions_form():
    """
    """
    # adf_questions = st.session_state.atomic_defake.get_ai_questions()
    adf_questions = st.session_state.atomic_defake.get_ai_questions_fake()

    st.divider()

    with st.form(key="questions_form"):

        for idx in range(5):
            # if idx > 0:
            #     st.divider()

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
            options=["Trustworthy", "Somewhat trustworthy", "I don't know", "Not trustworthy"],
        )
    
        confidence = st.select_slider(
            "How confident are you in your answers?",
            # options=range(0, 101)
            options=[
                "very uncertain",
                "uncertain",
                "neither certain nor uncertain",
                "certain",
                "very certain"
            ],
        )

        st.session_state.contributor_conf = confidence

        submit_button = st.form_submit_button(
            label="Submit",
            on_click=send_answers_to_adf,
        )



            


############################################################################
st.title("Atomic-DeFake")
st.header("Contributor")
st.divider()

if st.session_state.stage != "contributor":
    st.text("""
        There is no post for you to review. 
        You will be notified when the post of another user is ready to be reviewed.
        """
        )
else:
    st.text("""
        Please answer to the list of questions below 
        to identify if any misleading information is present in the following post.
        """)
    
    if "post" in st.session_state:
        st.text(st.session_state.post)


    questions_form()


    