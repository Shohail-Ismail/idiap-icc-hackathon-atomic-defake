import streamlit as st

def set_atomic_defake():
    """API fo Atomic DeFake"""
    st.session_state.stage = "atomic_defake"

def preamble():
    st.title("AtomicDeFake")
    social_media_buttons()

def social_media_on_click(idx, SOCIAL_MEDIA, SOCIAL_MEDIA_CHARS):
    """ """
    social_media_item = {"name": "", "max_chars": 0}

    social_media_item["name"] = SOCIAL_MEDIA[idx].lower()
    social_media_item["max_chars"] = SOCIAL_MEDIA_CHARS[idx]

    st.session_state.social_media = social_media_item
    st.session_state.stage = "post"

def social_media_buttons():
    """ """

    st.text("Where do you want to post?")
    st.divider()

    # TODO - move to a file to read maybe? Make sure to read once before running the app
    SOCIAL_MEDIA = ["Facebook", "Twitter", "Linkedin", "Other"]
    SOCIAL_MEDIA_CHARS = [63206, 280, 280, 280]

    n_buttons = len(SOCIAL_MEDIA)

    assert n_buttons == 4
    col1, col2, col3, col4 = st.columns([1] * n_buttons)

    with col1:
        idx = 0
        if st.button(SOCIAL_MEDIA[idx]):
            social_media_on_click(idx, SOCIAL_MEDIA, SOCIAL_MEDIA_CHARS)

    with col2:
        idx = 1
        if st.button(SOCIAL_MEDIA[idx]):
            social_media_on_click(idx, SOCIAL_MEDIA, SOCIAL_MEDIA_CHARS)

    with col3:
        idx = 2
        if st.button(SOCIAL_MEDIA[idx]):
            social_media_on_click(idx, SOCIAL_MEDIA, SOCIAL_MEDIA_CHARS)

    with col4:
        idx = 3
        if st.button(SOCIAL_MEDIA[idx]):
            social_media_on_click(idx, SOCIAL_MEDIA, SOCIAL_MEDIA_CHARS)

def post_message(message_form):
    st.divider()

    n_max_chars_social = st.session_state.social_media["max_chars"]

    with st.form(key="post_form"):
        st.text_area(
            message_form,
            value="",
            height=None,
            max_chars=n_max_chars_social,
            key="post",
            help=None,
            on_change=None,
            args=None,
            label_visibility="visible",
        )

        submit_button = st.form_submit_button(
            label="AtomicDeFake",
            on_click=set_atomic_defake,
        )

def run_atomic_defake():
    """ """
    user_post = st.session_state.post

    st.divider()
    st.text(
        "Wait for your post to be certified before being posted to {:s}".format(
            st.session_state.social_media["name"]
        )
    )

    st.session_state.atomic_defake.verify_ai(user_post)

    if st.session_state.atomic_defake.get_status() == "human_responses":
        st.session_state.stage = "contributor"
        st.session_state.post = user_post
        st.switch_page("contributor.py")

def set_output_stage():
    st.divider()
    assigned_adf_label, user_response = st.session_state.atomic_defake.get_output()

    if assigned_adf_label == 1:
        st.text("Here is your certified output:\n")
        st.write(user_response)

        st.session_state.stage = None
        st.session_state.atomic_defake.reset()

    elif assigned_adf_label == 0:
        st.text("Your post has not been verified because of the following reasons:\n")
        st.write(user_response)

        st.session_state.stage = "edit"

# APP FLOW

preamble()

if st.session_state.stage == "post":
    st.session_state.n_checkers_iter = st.session_state.n_checkers
    post_message("Write your post here")

if st.session_state.stage == "atomic_defake":
    run_atomic_defake()

if st.session_state.stage == "output":
    set_output_stage()

    if st.session_state.stage == "edit":
        st.session_state.n_checkers_iter = st.session_state.n_checkers
        st.session_state.atomic_defake.reset()
        post_message("Edit your post here and submit again for verification.")
    else:
        st.session_state.stage = None
        st.session_state.atomic_defake.reset()
