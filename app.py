import streamlit as st
from views import welcome, population


def main():

    # Set page config for a wider layout
    st.set_page_config(layout="wide")

    if 'page' not in st.session_state:
        st.session_state.page = "welcome"

    # Apply custom CSS
    with open("static/css/styles.css") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    if st.session_state.page == "welcome":
        welcome.show()
    elif st.session_state.page == "population":
        population.show()
    else:
        st.write(f"Page for {st.session_state.page} is under construction.")
        if st.button("Back to Welcome Page", use_container_width=True):
            st.session_state.page = "welcome"
            st.rerun()


if __name__ == "__main__":
    main()
