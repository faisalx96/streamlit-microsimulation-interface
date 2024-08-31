import streamlit as st
from utils.data_processing import filter_data, get_combination
from utils.plots import plot_population_projection, plot_population_composition


def show_comparison_mode(df, combination1, combination2):
    # st.subheader("Scenario Comparison")
    
    # Get data for both scenarios
    filtered_df1 = filter_data(df, combination1)
    
    filtered_df2 = filter_data(df, combination2)
    
    # Create the base figure using the imported function
    fig = plot_population_projection(filtered_df1, False)
    
    # Modify the existing trace for Scenario 1
    fig.data[0].update(
        name=f"Scenario 1",
        line=dict(color='#00FFFF', width=2),  # Vibrant cyan
        showlegend=True
    )
    
    # Add a new trace for Scenario 2
    fig.add_trace(
        plot_population_projection(filtered_df2, False).data[0]
    )
    
    # Modify the new trace for Scenario 2
    fig.data[1].update(
        name=f"Scenario 2",
        line=dict(color='#FFA500', width=2),  # Warm orange
        showlegend=True
    )
    
    # Update layout to ensure legend is shown and transparent, with light text
    fig.update_layout(
        showlegend=True,
        legend=dict(
            # yanchor="top",
            # y=0.99,
            # xanchor="left",
            # x=0.01,
            bgcolor="rgba(0,0,0,0)",  # Transparent background
            bordercolor="rgba(0,0,0,0)",  # Transparent border
            font=dict(color="white")  # White text for visibility on dark background
        ),
        # margin=dict(t=50, l=50, r=50, b=50),  # Add margins for better spacing
        paper_bgcolor="rgba(0,0,0,0)",  # Transparent background
        plot_bgcolor="rgba(0,0,0,0)",  # Transparent background
        font=dict(color="white")  # White text for all labels
    )
    
    # Update axes for better visibility on dark background
    fig.update_xaxes(gridcolor="gray", zerolinecolor="gray")
    fig.update_yaxes(gridcolor="gray", zerolinecolor="gray")
    
    # Display the figure
    st.plotly_chart(fig, use_container_width=True, config={'displayModeBar': False})

    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # Population composition charts (unchanged)
    comp_year = 2100
    col1, col2 = st.columns(2)

    with col1:
        # st.subheader(f"Scenario 1 Population Composition")
        comp_fig1 = plot_population_composition(filtered_df1, comp_year, title=f"Scenario 1 Population Composition at {comp_year}")
        st.plotly_chart(comp_fig1, use_container_width=True, config={'displayModeBar': False})

    with col2:
        # st.subheader(f"Scenario 2 Population Composition")
        comp_fig2 = plot_population_composition(filtered_df2, comp_year, title=f"Scenario 2 Population Composition at {comp_year}")
        st.plotly_chart(comp_fig2, use_container_width=True, config={'displayModeBar': False})