import streamlit as st
import pandas as pd
import numpy as np
import random
import time


STATUSES = ["wait", "completed", "start"]

class AtomicDeFake():
    def __init__(self):
        self.status="start"
        self.user_post=""



    def get_status(self):
        return self.status

    def get_output(self):
        return self.user_post

    def set_status(self, status):
        """
        """
        assert(status in STATUSES)
        self.status = status

    def run(self, user_post, threshold=0.8):
        """
        """
        self.set_status("wait")

        likelihood = random.random()
        
        if likelihood > threshold:
            label = True
            user_post = user_post + "\n\nPassed Atomic-DeFake check."
        else:
            label = False
            user_post = "Failed Atomic-DeFake check."

        time.sleep(3)
        
        self.user_post = user_post

        self.set_status("completed")



def run_atomic_defake(atomic_defake, user_post):
    set_atomic_defake()

    st.divider()
    st.text("Wait for your post to be certified before being posted to {:s}".format(st.session_state.social_media["name"]))
    
    atomic_defake.run(user_post)

    if atomic_defake.get_status() == "completed":
        st.session_state.stage = "output"



def set_atomic_defake():
    """ API fo Atomic DeFake
    """
    st.session_state.stage = "atomic_defake"

def set_output_stage(atomic_defake):
    # 

    # preamble(atomic_defake)
    st.divider()
    st.text("Here is your certified output")
    st.text(atomic_defake.get_output())


def show_post(n_max_chars_social, atomic_defake):
    """
    """
    # st.divider()

    with st.form(key='post_form'):
        st.text_area("Write your post here", value="", height=None, 
            max_chars=n_max_chars_social, key="post", 
            help=None, on_change=None, args=None, label_visibility="visible")
        
        submit_button = st.form_submit_button(label='Atomic-DeFake', 
            on_click=run_atomic_defake  , args=(atomic_defake, st.session_state.post,)
            )


def preamble(atomic_defake):
    st.title('Atomic-DeFake')
    st.divider()
    
    st.text("Where do you want to post?")
    social_media_buttons(atomic_defake)        


def initialise_session():
    """
    """
    if "stage" not in st.session_state:
        st.session_state.stage = None

    if 'social_media' not in st.session_state:
        st.session_state.social_media = None

def reset_session():
    """
    """
    if 'social_media' not in st.session_state:
        st.session_state.social_media = None



def social_media_buttons(atomic_defake):
    """
    """
    # st.session_state.stage = "social media button"

    SOCIAL_MEDIA = ["Facebook", "Twitter", "Linkedin", "Other"]
    SOCIAL_MEDIA_CHARS = [63206, 280, 280, 280]

    n_buttons = len(SOCIAL_MEDIA)
    col1, col2, col3, col4 = st.columns([1]*n_buttons)
    
    social_media_item = {"name":"", "max_chars":0}

    with col1:
        idx = 0
        if st.button(SOCIAL_MEDIA[idx]): 
            social_media_item['name'] = SOCIAL_MEDIA[idx].lower()
            social_media_item['max_chars']=SOCIAL_MEDIA_CHARS[idx]
            
            st.session_state.social_media=social_media_item
            st.session_state.stage="post"
            
    with col2:
        idx = 1
        if st.button(SOCIAL_MEDIA[idx]): 
            social_media_item['name'] = SOCIAL_MEDIA[idx].lower()
            social_media_item['max_chars']=SOCIAL_MEDIA_CHARS[idx]
            
            st.session_state.social_media=social_media_item
            st.session_state.stage="post"
            
    with col3:    
        idx = 2
        if st.button(SOCIAL_MEDIA[idx]): 
            social_media_item['name'] = SOCIAL_MEDIA[idx].lower()
            social_media_item['max_chars']=SOCIAL_MEDIA_CHARS[idx]
            
            st.session_state.social_media=social_media_item
            st.session_state.stage="post"

    with col4:
        idx = 3
        if st.button(SOCIAL_MEDIA[idx]): 
            social_media_item['name'] = SOCIAL_MEDIA[idx].lower()
            social_media_item['max_chars']=SOCIAL_MEDIA_CHARS[idx]
            
            st.session_state.social_media=social_media_item
            st.session_state.stage="post"


def post_message(atomic_defake):
    st.divider()
    show_post(st.session_state.social_media['max_chars'], atomic_defake)




if __name__ == "__main__":

    initialise_session()

    atomic_defake = AtomicDeFake()

    # if not st.session_state.stage:
    preamble(atomic_defake)

    if st.session_state.stage=="post":
        post_message(atomic_defake)

    # if st.session_state.stage == "social media post":
    #     st.divider()
    #     show_post(st.session_state.social_media['max_chars'], atomic_defake)

    if st.session_state.stage == "output":
        set_output_stage(atomic_defake)
        

