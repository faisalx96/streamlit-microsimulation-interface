import streamlit as st
from components.custom_components import create_card


def show():
    st.title("Welcome to the National Microsimulation Engine")
    st.markdown("#### Explore different microsimulation topics:")

    col1, col2 = st.columns(2)

    with col1:
        create_card(
            "Population",
            "Analyze population dynamics, demographics, and future projections.",
            "https://www.state.gov/wp-content/uploads/2023/07/shutterstock_1938189982v2.jpg",
            "population"
        )

        create_card(
            "Military Retirement",
            "Simulate retirement scenarios for military personnel and impact on government spend.",
            "https://www.leaders-mena.com/leaders/uploads/2021/01/Saudi-Army.jpg",
            "military_retirement"
        )

    with col2:
        create_card(
            "Labor Market Dynamics",
            "Explore employment trends, wage dynamics, and workforce projections.",
            "https://saudigazette.com.sa/uploads/images/2023/04/25/2104678.jpeg",
            "labor_market"
        )

        create_card(
            "Taxation Policies",
            "Model various taxation policies and their economic impacts.",
            "https://admin.expatica.com/sa/wp-content/uploads/sites/14/2023/11/saudi-riyal-pile.jpg",
            "taxation"
        )
