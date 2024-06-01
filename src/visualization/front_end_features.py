import streamlit.components.v1 as components
import streamlit as st

def pop_up(CTA, title, body):
    with st.expander(CTA):
        st.title(title)
        st.markdown(body)