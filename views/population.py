import streamlit as st
from utils.data_processing import load_data, filter_data, get_combination
from components.custom_components import sidebar_custom_slider, custom_sidebar_button
from components.chatgpt_dialog import show_ui
from views.scenario_comparison import show_comparison_mode
from utils.plots import plot_population_projection, plot_population_composition

def show():
    st.title('Population Microsimulation')

    # Load data
    df = load_data()

    # Toggle for comparison mode
    comparison_mode = st.sidebar.checkbox("Enable Scenario Comparison")

    # Initialize generating_projection state if it doesn't exist
    if 'generating_projection' not in st.session_state:
        st.session_state.generating_projection = False

    # Display ChatGPT dialog in main area if generating
    if st.session_state.get('generating_projection', False):
        show_ui()
        return

    if comparison_mode:
        # Scenario 1
        st.sidebar.markdown("### Scenario 1")
        combinations = df['Combination'].unique()
        other_combinations = [c for c in combinations if not (c.startswith('asmr'))]
        selected_combination1 = st.sidebar.selectbox('Scenarios 1', ['None'] + other_combinations, key='scenario1')

        asmr1 = sidebar_custom_slider('Mortality', -5, 5, 0, 'asmr1', 'Low', 'High')
        asfr1 = sidebar_custom_slider('Fertility', -5, 4, 0, 'asfr1', 'Low', 'High')
        slider_combination1 = get_combination(asmr1, asfr1)

        combination1 = selected_combination1 if selected_combination1 != 'None' else slider_combination1
        st.sidebar.markdown("---")

        # Scenario 2
        st.sidebar.markdown("### Scenario 2")
        selected_combination2 = st.sidebar.selectbox('Scenarios 2', ['None'] + other_combinations, key='scenario2')

        asmr2 = sidebar_custom_slider('Mortality', -5, 5, 0, 'asmr2', 'Low', 'High')
        asfr2 = sidebar_custom_slider('Fertility', -5, 4, 0, 'asfr2', 'Low', 'High')
        slider_combination2 = get_combination(asmr2, asfr2)

        combination2 = selected_combination2 if selected_combination2 != 'None' else slider_combination2
        st.sidebar.markdown("---")

        show_comparison_mode(df, combination1, combination2)
    else:
        # Sidebar for user inputs and ChatGPT dialog
        st.sidebar.header('Instruments')
        combinations = df['Combination'].unique()
        other_combinations = [c for c in combinations if not (c.startswith('asmr'))]

        # Scenarios dropdown
        selected_combination = st.sidebar.selectbox('Scenarios', ['None'] + other_combinations)

        # Sliders for ASMR and ASFR
        asmr = sidebar_custom_slider('Mortality', -5, 5, 0, 'asmr', 'Low', 'High')
        asfr = sidebar_custom_slider('Fertility', -5, 4, 0, 'asfr', 'Low', 'High')
        slider_combination = get_combination(asmr, asfr)

        # Determine which combination to use
        combination = selected_combination if selected_combination != 'None' else slider_combination

        show_single_mode(df, combination, True)

        # Add ChatGPT Dialog to sidebar only in single mode
        st.sidebar.markdown("---")
        show_ui()

        st.sidebar.markdown("---")

    # Custom sidebar back button
    if custom_sidebar_button("Back to Home Page", "sidebar_back_button"):
        st.session_state.page = "welcome"
        st.rerun()

def show_single_mode(df, combination, show_base_projection):
    filtered_df = filter_data(df, combination)

    # Display charts in main area
    if 'generated_df' in st.session_state:
        st.plotly_chart(plot_population_projection(st.session_state.generated_df, show_base_projection, is_generated=True),
                        use_container_width=True, config={'displayModeBar': False})
    else:
        st.plotly_chart(plot_population_projection(filtered_df, show_base_projection),
                        use_container_width=True, config={'displayModeBar': False})

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    if 'generated_df' not in st.session_state:
        col1, col_divider, col2 = st.columns([10, 1, 10])

        with col1:
            st.plotly_chart(plot_population_composition(filtered_df, 2024, title=f"Population Composition at 2024"), use_container_width=True,
                            config={'displayModeBar': False})

        with col_divider:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        with col2:
            st.plotly_chart(plot_population_composition(filtered_df, 2100, title=f"Population Composition at 2100"), use_container_width=True,
                            config={'displayModeBar': False})