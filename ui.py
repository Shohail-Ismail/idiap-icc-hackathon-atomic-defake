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
import argparse
import streamlit as st

from atomic_defake.atomic_defake import AtomicDeFake

UI_STAGES = ["atomic_defake", "post", "adf_aggregation", "contributor", "output"]


def initialise_session():
    """ """
    st.session_state.stage = None

    if "social_media" not in st.session_state:
        st.session_state.social_media = None

    st.session_state.atomic_defake = AtomicDeFake(
        aggregation_method="single_false_or_unsure"
    )


def reset_session():
    """ """
    if "stage" not in st.session_state:
        st.session_state.stage = None

    if "social_media" not in st.session_state:
        st.session_state.social_media = None


if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login():
    if st.button("Log in"):
        st.session_state.logged_in = True
        st.rerun()


def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()


if __name__ == "__main__":

    if "stage" not in st.session_state:
        initialise_session()

    login_page = st.Page(login, title="Log in", icon=":material/login:")
    logout_page = st.Page(logout, title="Log out", icon=":material/logout:")

    user_post_page = st.Page(
        "user_post.py", title="User post", icon=":material/add_circle:"
    )
    contributor_page = st.Page(
        "contributor.py", title="Contributor", icon=":material/delete:"
    )

    if st.session_state.logged_in:
        pg = st.navigation(
            {
                "Account": [logout_page],
                "AtomicDeFake": [user_post_page, contributor_page],
            }
        )
        st.set_page_config(
            page_title="Atomic-DeFake", page_icon=":identification_card:"
        )

    else:
        pg = st.navigation([login_page])

    pg.run()
