import streamlit as st


def create_card(title, description, image_path, page_name):
    card_html = f"""
    <div class="card">
        <img src={image_path}>
        <div class="card-content">
            <div class="card-title">{title}</div>
            <div class="card-description">{description}</div>
        </div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

    if st.button("", key=f"button_{page_name}", use_container_width=True):
        st.session_state.page = page_name
        st.rerun()


def sidebar_custom_slider(label, min_value, max_value, value, key, min_label, max_label):
    st.sidebar.write(label)
    col1, col2, col3 = st.sidebar.columns([2, 8, 2])
    with col1:
        st.write(min_label)
    with col2:
        value = st.slider('', min_value, max_value, value, key=key, label_visibility='collapsed')
    with col3:
        st.write(max_label)
    return value


def custom_sidebar_button(label: str, key: str):
    clicked = st.sidebar.button(label, key=key, use_container_width=True)

    # Apply custom styling to the button
    st.sidebar.markdown(
        f"""
        <style>
        div[data-testid="stButton"] > button {{
            background-color: rgb(14, 17, 23);
            color: white;
            font-weight: bold;
            border: none;
            padding: 10px 15px;
            border-radius: 10px;
            min-height: 1rem !important;
            margin-top: 0px !important;
            position: relative !important;
            transition: background-color 0.3s ease, transform 0.2s ease;
        }}
        div[data-testid="stButton"] > button:hover {{
            background-color: rgb(14, 17, 23);
            transform: translateY(-2px);
        }}
        div[data-testid="stButton"] > button:active {{
            transform: translateY(0px);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    return clicked
