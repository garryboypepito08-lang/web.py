import plotly.graph_objects as go


def make_status_donut(values):
    labels = ["In Progress", "On Hold", "Not Started"]
    vals = [values.get("In Progress", 0), values.get("On Hold", 0), values.get("Not Started", 0)]
    fig = go.Figure(
        data=[go.Pie(
            labels=labels,
            values=vals,
            hole=0.65,
            marker=dict(colors=["#00FF99", "#FFD166", "#A9B6C1"], line=dict(color="rgba(255,255,255,0.12)", width=1)),
            textinfo='value',
            textfont=dict(color='white', size=16),
            hoverinfo='label+percent',
            showlegend=True,
            direction='clockwise'
        )]
    )
    fig.update_layout(
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=0, r=0, t=0, b=0),
        legend=dict(font=dict(color='white'), orientation='v', x=1.1, y=0.8),
        font=dict(color='white')
    )
    return fig
