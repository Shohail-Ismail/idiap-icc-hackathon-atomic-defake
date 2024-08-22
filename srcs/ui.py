import streamlit as st
import pandas as pd
import numpy as np
import random
import time



def set_atomic_defake():
    """ API fo Atomic DeFake
    """
    st.session_state.atomic_defake = True


def show_post(n_max_chars_social):
    st.divider()

    with st.form(key='post_form'):
        st.text_area("Write your post here", value="", height=None, 
            max_chars=n_max_chars_social, key="post", 
            help=None, on_change=None, args=None, label_visibility="visible")
        
        submit_button = st.form_submit_button(label='Atomic-DeFake', 
            on_click=set_atomic_defake)

    return submit_button



def run_AtomicDeFake(user_post):
    """
    """
    # st.status("Atomic-DeFake", *, expanded=False, state="running")

    likelihood = random.random()
    
    if likelihood > 0.8:
        label = True
        user_post = user_post + "\n\nPassed Atomic-DeFake check."
    else:
        label = False
        user_post = "Failed Atomic-DeFake check."

    time.sleep(3)

    st.session_state.message = True
    
    return label, user_post


def initialise_session():
    if 'atomic_defake' not in st.session_state:
        st.session_state.atomic_defake = False

    if 'message' not in st.session_state:
        st.session_state.message = False



if __name__ == "__main__":

    initialise_session()


    st.title('Atomic-DeFake')
    st.divider()

    st.text("Where do you want to post?")

    social_media_name=None

    col1, col2, col3, col4 = st.columns([1,1,1,1])
    with col1:
        if st.button("Facebook"): 
            n_max_chars_social=63206
            social_media_name="facebook"
            
    with col2:
        if st.button("Twitter"):
            n_max_chars_social=280
            social_media_name="twitter"
            
    with col3:    
        if st.button("Linkedin"):
            n_max_chars_social=280
            social_media_name="linkedin"

    with col4:    
        if st.button("Other"):
            n_max_chars_social=280
            social_media_name="other"

    if social_media_name:
        submit_button = show_post(n_max_chars_social)
    

    if st.session_state.atomic_defake:
        label, user_post = run_AtomicDeFake(st.session_state.post)
    
    if st.session_state.message:
        st.divider()
        st.session_state.post
        st.text("Passed Atomic-DeFake check")
