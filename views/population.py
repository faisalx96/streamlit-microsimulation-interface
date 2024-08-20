import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from utils.data_processing import load_data, filter_data, get_combination, format_number
from components.custom_components import sidebar_custom_slider, custom_sidebar_button
from components.chatgpt_dialog import show_chatgpt_dialog


def show():
    st.title('Population Microsimulation Engine')

    # Sidebar for user inputs and ChatGPT dialog
    st.sidebar.header('Instruments')

    # Original controls
    df = load_data()
    combinations = df['Combination'].unique()
    other_combinations = [c for c in combinations if not (c.startswith('asmr'))]
    selected_combination = st.sidebar.selectbox('Scenarios', ['None'] + other_combinations)
    asmr = sidebar_custom_slider('Mortality', -5, 5, 0, 'asmr', 'Worse', 'Better')
    asfr = sidebar_custom_slider('Fertility', -5, 5, 0, 'asfr', 'Worse', 'Better')
    slider_combination = get_combination(asmr, asfr)
    combination = selected_combination if selected_combination != 'None' else slider_combination
    filtered_df = filter_data(df, combination)

    # Add ChatGPT Dialog to sidebar
    st.sidebar.markdown("---")
    show_chatgpt_dialog()

    # Display charts in main area
    if 'generated_df' in st.session_state:
        st.plotly_chart(plot_population_projection(st.session_state.generated_df, is_generated=True),
                        use_container_width=True, config={'displayModeBar': False})
    else:
        st.plotly_chart(plot_population_projection(filtered_df),
                        use_container_width=True, config={'displayModeBar': False})

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Only show composition charts for original data
    if 'generated_df' not in st.session_state:
        col1, col_divider, col2 = st.columns([10, 1, 10])

        with col1:
            st.plotly_chart(plot_population_composition(filtered_df, 2024), use_container_width=True,
                            config={'displayModeBar': False})

        with col_divider:
            st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

        with col2:
            st.plotly_chart(plot_population_composition(filtered_df, 2100), use_container_width=True,
                            config={'displayModeBar': False})

    # Custom sidebar back button
    st.sidebar.markdown("---")
    if custom_sidebar_button("Back to Home Page", "sidebar_back_button"):
        st.session_state.page = "welcome"
        st.rerun()


def plot_population_projection(df, is_generated=False):
    if is_generated:
        fig = px.line(df, x='Year', y='Population', title='Population Projection (AI Generated)')
    else:
        yearly_data = df.groupby('Year')['Count'].sum().reset_index()
        yearly_data['Count'] = yearly_data['Count'] * 19.5 * 10  # Adjust as needed
        fig = px.line(yearly_data, x='Year', y='Count', title='Population Projection')

    fig.update_layout(
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#444',
        title_font_size=20,
        xaxis_title_font_size=16,
        yaxis_title_font_size=16,
        height=500,
        xaxis=dict(
            showgrid=False,
            tickmode='array',
            tickvals=list(range(2024, 2101, 10)),
            tickangle=0,
            tickfont=dict(size=14)
        ),
        yaxis=dict(title='Population', showgrid=False, tickfont=dict(size=14))
    )
    return fig


def plot_population_composition(all_df, year):
    df = all_df[all_df['Year'] == year]
    male_data = df[df['Gender'] == 'M'].sort_values('AgeGroup')
    female_data = df[df['Gender'] == 'F'].sort_values('AgeGroup')

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=male_data['AgeGroup'],
        x=male_data['Count'] * 195,
        name='Male',
        orientation='h',
        marker_color='#1e3799'
    ))
    fig.add_trace(go.Bar(
        y=female_data['AgeGroup'],
        x=-female_data['Count'] * 195,
        name='Female',
        orientation='h',
        marker_color='#b71540'
    ))
    fig.update_layout(
        title=f'Population Composition at {year}',
        barmode='relative',
        yaxis=dict(title=None, showgrid=False, tickfont=dict(size=14)),
        xaxis=dict(title=None, showgrid=False, showticklabels=False, zeroline=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='#444',
        title_font_size=20,
        xaxis_title_font_size=16,
        showlegend=False,
        height=500,
    )

    max_count = max(male_data['Count'].max() * 195, female_data['Count'].max() * 195)

    for i, m in enumerate(male_data['Count'] * 195):
        x_pos = m if m / max_count < 0.15 else m / 2
        align = 'left' if m / max_count < 0.15 else 'center'
        fig.add_annotation(
            x=x_pos, y=i,
            text=format_number(m),
            showarrow=False,
            font=dict(color='white', size=12),
            xanchor=align
        )

    for i, f in enumerate(female_data['Count'] * 195):
        x_pos = -f if f / max_count < 0.15 else -f / 2
        align = 'right' if f / max_count < 0.15 else 'center'
        fig.add_annotation(
            x=x_pos, y=i,
            text=format_number(f),
            showarrow=False,
            font=dict(color='white', size=12),
            xanchor=align
        )

    return fig
