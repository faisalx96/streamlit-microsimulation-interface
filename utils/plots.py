import plotly.express as px
import plotly.graph_objects as go
from utils.data_processing import load_data, filter_data, format_number


def plot_population_projection(df, show_base_projection, is_generated=False):

    if is_generated:
        fig = px.line(df, x='Year', y='Population', title='Population Projection (AI Generated)')
    else:
        yearly_data = df.groupby('Year')['Count'].sum().reset_index()
        yearly_data['Count'] = yearly_data['Count'] * 19 * 10  # Adjust as needed
        fig = px.line(yearly_data, x='Year', y='Count', title='Population Projection')
    
    if show_base_projection:
        # Add reference line for asmr_0_asfr_0
        reference_df = filter_data(load_data(), 'asmr_0_asfr_0')
        reference_data = reference_df.groupby('Year')['Count'].sum().reset_index()
        reference_data['Count'] = reference_data['Count'] * 19 * 10
        fig.add_trace(go.Scatter(
            x=reference_data['Year'],
            y=reference_data['Count'],
            mode='lines',
            name='Base Projection',
            line=dict(color='rgb(0, 255, 127)')
        ))

    fig.update_layout(
        showlegend=True,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
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

def plot_population_composition(all_df, year, title):
    df = all_df[all_df['Year'] == year]
    male_data = df[df['Gender'] == 'M'].sort_values('AgeGroup')
    female_data = df[df['Gender'] == 'F'].sort_values('AgeGroup')

    fig = go.Figure()
    fig.add_trace(go.Bar(
        y=male_data['AgeGroup'],
        x=male_data['Count'] * 19,
        name='Male',
        orientation='h',
        marker_color='#1e3799'
    ))
    fig.add_trace(go.Bar(
        y=female_data['AgeGroup'],
        x=-female_data['Count'] * 19,
        name='Female',
        orientation='h',
        marker_color='#b71540'
    ))
    fig.update_layout(
        title=title,
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

    max_count = max(male_data['Count'].max() * 19, female_data['Count'].max() * 19)

    for i, m in enumerate(male_data['Count'] * 19):
        x_pos = m if m / max_count < 0.15 else m / 2
        align = 'left' if m / max_count < 0.15 else 'center'
        fig.add_annotation(
            x=x_pos, y=i,
            text=format_number(m),
            showarrow=False,
            font=dict(color='white', size=12),
            xanchor=align
        )

    for i, f in enumerate(female_data['Count'] * 19):
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