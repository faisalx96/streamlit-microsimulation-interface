import pandas as pd
import streamlit as st
from utils.data_processing import load_data, filter_data, get_combination
from components.custom_components import sidebar_custom_slider, custom_sidebar_button
from components.chatgpt_dialog import show_ui
from views.scenario_comparison import show_comparison_mode
from utils.plots import plot_population_projection, plot_population_composition
import plotly.graph_objects as go
import numpy as np


def show():
    st.title('Population Microsimulation')

    # Load data
    df = load_data()

    # Create tabs
    tab1, tab2 = st.tabs(["Scenario Analysis", "Sensitivity Analysis"])

    with tab1:
        show_scenario_analysis(df)

    with tab2:
        show_sensitivity_analysis(df)

    # Custom sidebar back button (outside of tabs)
    if custom_sidebar_button("Back to Home Page", "sidebar_back_button"):
        st.session_state.page = "welcome"
        st.rerun()


def show_scenario_analysis(df):

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
        st.markdown('### Scenario Comparison Mode')
        st.sidebar.markdown('# Instruments')
        # Scenario 1
        st.sidebar.markdown("### Scenario 1")
        combinations = df['Combination'].unique()
        other_combinations = [c for c in combinations if not (c.startswith('asmr'))]
        selected_combination1 = st.sidebar.selectbox('Select a specific scenario', ['None'] + other_combinations, key='scenario1')

        asmr1 = sidebar_custom_slider('Mortality', -5, 5, 0, 'asmr1', 'Low', 'High')
        asfr1 = sidebar_custom_slider('Fertility', -5, 4, 0, 'asfr1', 'Low', 'High')
        slider_combination1 = get_combination(asmr1, asfr1)

        combination1 = selected_combination1 if selected_combination1 != 'None' else slider_combination1
        st.sidebar.markdown("---")

        # Scenario 2
        st.sidebar.markdown("### Scenario 2")
        selected_combination2 = st.sidebar.selectbox('Select a specific scenario', ['None'] + other_combinations, key='scenario2')

        asmr2 = sidebar_custom_slider('Mortality', -5, 5, 0, 'asmr2', 'Low', 'High')
        asfr2 = sidebar_custom_slider('Fertility', -5, 4, 0, 'asfr2', 'Low', 'High')
        slider_combination2 = get_combination(asmr2, asfr2)

        combination2 = selected_combination2 if selected_combination2 != 'None' else slider_combination2
        st.sidebar.markdown("---")

        show_comparison_mode(df, combination1, combination2)
    else:
        # Sidebar for user inputs and ChatGPT dialog
        st.sidebar.markdown('# Instruments')
        combinations = df['Combination'].unique()
        other_combinations = [c for c in combinations if not (c.startswith('asmr'))]

        # Scenarios dropdown
        selected_combination = st.sidebar.selectbox('Select a specific scenario', ['None'] + other_combinations)

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


def show_sensitivity_analysis(df):
    # Generate all combinations of ASMR and ASFR
    asmr_values = range(-5, 6)
    asfr_values = range(-5, 5)

    # Create empty matrix to store results
    results = np.zeros((len(asmr_values), len(asfr_values)))

    # Perform analysis
    for i, asmr in enumerate(asmr_values):
        for j, asfr in enumerate(asfr_values):
            combination = get_combination(asmr, asfr)
            filtered_df = filter_data(df, combination)

            # Calculate a metric (e.g., total population in 2100)
            metric = filtered_df[filtered_df['Year'] == 2100]['Count'].sum() * 190

            results[i, j] = metric

    # Create heatmap
    fig = go.Figure(data=go.Heatmap(
        z=results,
        x=list(asfr_values),
        y=list(asmr_values),
        colorscale='Viridis',
        colorbar=dict(
            titleside='right',
            tickfont=dict(size=16)
        )
    ))

    fig.update_layout(
        xaxis_title='Fertility',
        yaxis_title='Mortality',
        xaxis_title_font_size=24,
        yaxis_title_font_size=24,
        width=800,
        height=600,
        margin=dict(t=20, b=20, l=70, r=20),  # Adjust top margin
        xaxis=dict(
            tickmode='array',
            tickvals=list(asfr_values),
            ticktext=list(asfr_values),
            tickfont=dict(size=18)

        ),
        yaxis=dict(
            tickmode='array',
            tickvals=list(asmr_values),
            ticktext=list(asmr_values),
            tickfont=dict(size=18)

        )
    )

    st.markdown("## Sensitivity Analysis: Population in 2100")
    # Display the chart
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    # Additional insights
    st.write("### Key Insights:")

    max_index = np.unravel_index(results.argmax(), results.shape)
    min_index = np.unravel_index(results.argmin(), results.shape)

    st.write(f"1. **Population Range**: The projected population in 2100 ranges from a minimum of {results.min():,.0f} "
             f"(Mortality = {asmr_values[min_index[0]]}, Fertility = {asfr_values[min_index[1]]}) to a maximum of {results.max():,.0f} "
             f"(Mortality = {asmr_values[max_index[0]]}, Fertility = {asfr_values[max_index[1]]}).")

    st.write(f"2. **Sensitivity**: The population projection is most sensitive to changes in fertility rates, "
             f"as indicated by the more dramatic color changes along the horizontal axis. Mortality rates "
             f"also impact the projection, but to a lesser extent, as seen by the more gradual color changes vertically.")

    st.markdown("---")

    st.markdown("## Sensitivity Analysis: Policy Impact vs Population Volatility")

    # Generate all combinations of ASMR and ASFR
    asmr_values = range(-5, 6)
    asfr_values = range(-5, 5)

    # Calculate baseline (no change scenario)
    baseline_combination = get_combination(0, 0)
    baseline_df = filter_data(df, baseline_combination)
    baseline_population_2100 = baseline_df[baseline_df['Year'] == 2100]['Count'].sum() * 190

    res = []

    for i, asmr in enumerate(asmr_values):
        for j, asfr in enumerate(asfr_values):
            combination = get_combination(asmr, asfr)
            filtered_df = filter_data(df, combination)

            # Calculate population for each year
            yearly_populations = [filtered_df[filtered_df['Year'] == year]['Count'].sum() * 190 for year in
                                  range(2024, 2101)]

            # Calculate final impact
            final_population = yearly_populations[-1]
            impact = (final_population - baseline_population_2100) / baseline_population_2100
            # impact_matrix[i, j] = impact

            # Calculate volatility (standard deviation of year-over-year changes)
            yoy_changes = [(yearly_populations[i] - yearly_populations[i - 1]) / yearly_populations[i - 1] for i in
                           range(1, len(yearly_populations))]
            volatility = np.std(yoy_changes)
            # volatility_matrix[i, j] = volatility
            res.append({
                "ASMR": asmr,
                "ASFR": asfr,
                "impact": impact,
                "volatility": volatility,
                "strength":-asmr + asfr
            })
    odf = pd.DataFrame(res)
    # Create the scatter plot
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=odf['impact'],
        y=odf['volatility'],
        mode='markers',
        marker=dict(
            size=10,
            color=odf['strength'],  # Color based on combined policy strength
            colorscale='RdYlBu',
            colorbar=dict(
                title="Policy Strength",
                tickmode='array',
                tickvals=list(range(-10, 12, 2)),  # Adjust range as needed
                # ticktext=[str(i) for i in range(-10, 11, 2)],
                tickfont=dict(size=14),
                len=0.75,  # Adjust length of colorbar
                thickness=20,  # Adjust thickness of colorbar
                x=1.05,  # Adjust position of colorbar
            ),
            showscale=True
        ),
        hovertext="ASMR: " + odf['ASMR'].astype(str) + ", ASFR: " + odf['ASFR'].astype(str),  # Passing a DataFrame column as hover text
        hoverinfo='text'
    ))

    fig.update_layout(
        xaxis_title='Long-term Population Impact (% change from baseline)',
        yaxis_title='Population Volatility (Std Dev of YoY changes)',
        xaxis_title_font_size=20,
        yaxis_title_font_size=18,
        margin=dict(t=20, b=20, l=70, r=20),  # Adjust top margin
        width=800,
        height=600,
        showlegend=False,
        xaxis=dict(
            tickfont=dict(size=16)

        ),
        yaxis=dict(
            tickfont=dict(size=16)

        )
    )

    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown("""
    ### Key Insights:

    1. **Policy Effectiveness vs Stability Trade-off**: This chart reveals the relationship between the long-term impact of fertility and mortality policies (x-axis) and the volatility they introduce to population dynamics (y-axis).

    2. **Resilience Zones**: Policies in the lower-right quadrant are ideal, showing positive impact with low volatility. These represent resilient policy choices that produce stable, positive outcomes.

    3. **High-Risk, High-Reward Policies**: Points in the upper-right quadrant show policies with significant positive impact but high volatility. These might be effective but could lead to unpredictable population swings.

    4. **Counterproductive Policies**: The left side of the chart shows policies that reduce population compared to the baseline. If population growth is the goal, these would be counterproductive.

    5. **Policy Strength Insight**: The color gradient shows the combined strength of Mortality and Fertility policies. This shows if stronger policies always lead to better outcomes, or if there's a 'sweet spot' of policy intensity.
    """)


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