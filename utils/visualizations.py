import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

def create_trend_plot(df):
    """
    Create a trend plot for any numeric column over time if available.
    """
    # Try to find a date column
    date_col = None
    for col in df.columns:
        try:
            pd.to_datetime(df[col])
            date_col = col
            break
        except:
            continue
    
    if date_col is None:
        # If no date column, use index
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(df))),
            y=[1] * len(df),  # Dummy data
            mode='lines+markers',
            name='Data Points',
            line=dict(color='#2c3e50', width=3),
            marker=dict(size=8, color='#3498db')
        ))
    else:
        # If date column exists, use it
        df[date_col] = pd.to_datetime(df[date_col])
        monthly_counts = df.groupby(df[date_col].dt.to_period('M')).size().reset_index()
        monthly_counts[date_col] = monthly_counts[date_col].astype(str)
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_counts[date_col],
            y=monthly_counts[0],
            mode='lines+markers',
            name='Data Points',
            line=dict(color='#2c3e50', width=3),
            marker=dict(size=8, color='#3498db')
        ))
    
    fig.update_layout(
        title=dict(
            text='Data Trends Analysis',
            font=dict(size=20, color='#2c3e50')
        ),
        xaxis_title='Time Period',
        yaxis_title='Count',
        template='plotly_white',
        hovermode='x unified',
        showlegend=True,
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        font=dict(family="Arial, sans-serif", size=12, color="#2c3e50")
    )
    
    return fig.to_json()

def create_forecast_plot(df):
    """
    Create a forecast plot for any numeric column if available.
    """
    # Try to find a date column
    date_col = None
    for col in df.columns:
        try:
            pd.to_datetime(df[col])
            date_col = col
            break
        except:
            continue
    
    if date_col is None:
        # If no date column, create dummy forecast
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(len(df))),
            y=[1] * len(df),
            mode='lines',
            name='Data',
            line=dict(color='#2c3e50', width=3)
        ))
    else:
        # If date column exists, create actual forecast
        df[date_col] = pd.to_datetime(df[date_col])
        monthly_counts = df.groupby(df[date_col].dt.to_period('M')).size().reset_index()
        monthly_counts[date_col] = monthly_counts[date_col].astype(str)
        
        # Simple moving average forecast
        window = min(3, len(monthly_counts))
        forecast = monthly_counts[0].rolling(window=window).mean()
        
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=monthly_counts[date_col],
            y=monthly_counts[0],
            mode='lines+markers',
            name='Historical Data',
            line=dict(color='#2c3e50', width=3),
            marker=dict(size=8, color='#3498db')
        ))
        
        fig.add_trace(go.Scatter(
            x=monthly_counts[date_col],
            y=forecast,
            mode='lines',
            name='Forecast',
            line=dict(color='#e74c3c', width=3, dash='dash')
        ))
    
    fig.update_layout(
        title=dict(
            text='Data Forecast Analysis',
            font=dict(size=20, color='#2c3e50')
        ),
        xaxis_title='Time Period',
        yaxis_title='Count',
        template='plotly_white',
        hovermode='x unified',
        showlegend=True,
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        font=dict(family="Arial, sans-serif", size=12, color="#2c3e50")
    )
    
    return fig.to_json()

def create_salary_distribution(df):
    """
    Create a distribution plot for any numeric column.
    """
    # Find first numeric column
    numeric_col = None
    for col in df.columns:
        if df[col].dtype in ['int64', 'float64']:
            numeric_col = col
            break
    
    if numeric_col is None:
        # If no numeric column, create empty plot
        fig = go.Figure()
    else:
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df[numeric_col],
            nbinsx=20,
            marker_color='#3498db',
            opacity=0.75
        ))
    
    fig.update_layout(
        title=dict(
            text=f'{numeric_col if numeric_col else "Data"} Distribution',
            font=dict(size=20, color='#2c3e50')
        ),
        xaxis_title=numeric_col if numeric_col else 'Value',
        yaxis_title='Count',
        template='plotly_white',
        showlegend=False,
        height=300,
        margin=dict(l=50, r=50, t=80, b=50),
        font=dict(family="Arial, sans-serif", size=12, color="#2c3e50")
    )
    
    return fig.to_json()

def create_skills_analysis(df):
    """
    Create a bar chart for any categorical column.
    """
    # Find first categorical column
    cat_col = None
    for col in df.columns:
        if df[col].dtype == 'object':
            cat_col = col
            break
    
    if cat_col is None:
        # If no categorical column, create empty plot
        fig = go.Figure()
    else:
        # Count values in the column
        value_counts = df[cat_col].value_counts().head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=value_counts.values,
            y=value_counts.index,
            orientation='h',
            marker_color='#2c3e50'
        ))
    
    fig.update_layout(
        title=dict(
            text=f'Top 10 {cat_col if cat_col else "Categories"}',
            font=dict(size=20, color='#2c3e50')
        ),
        xaxis_title='Count',
        yaxis_title=cat_col if cat_col else 'Category',
        template='plotly_white',
        showlegend=False,
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        font=dict(family="Arial, sans-serif", size=12, color="#2c3e50")
    )
    
    return fig.to_json()

def create_location_distribution(df):
    """
    Create a bar chart for any location-like column.
    """
    # Try to find a location-like column
    location_col = None
    for col in df.columns:
        if col == 'location':
            location_col = col
            break
        elif df[col].dtype == 'object' and df[col].str.contains('city|location|place|address', case=False).any():
            location_col = col
            break
    
    if location_col is None:
        # If no location column, use first categorical column
        for col in df.columns:
            if df[col].dtype == 'object':
                location_col = col
                break
    
    if location_col is None:
        # If no suitable column, create empty plot
        fig = go.Figure()
    else:
        location_counts = df[location_col].value_counts().head(10)
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=location_counts.values,
            y=location_counts.index,
            orientation='h',
            marker_color='#2c3e50'
        ))
    
    fig.update_layout(
        title=dict(
            text=f'Top 10 {location_col if location_col else "Categories"}',
            font=dict(size=20, color='#2c3e50')
        ),
        xaxis_title='Count',
        yaxis_title=location_col if location_col else 'Category',
        template='plotly_white',
        showlegend=False,
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        font=dict(family="Arial, sans-serif", size=12, color="#2c3e50")
    )
    
    return fig.to_json()

def create_remote_vs_onsite(df):
    """
    Create a pie chart for any work type-like column.
    """
    # Try to find a work type-like column
    work_type_col = None
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].str.contains('remote|onsite|hybrid|work type', case=False).any():
            work_type_col = col
            break
    
    if work_type_col is None:
        # If no work type column, use first categorical column
        for col in df.columns:
            if df[col].dtype == 'object':
                work_type_col = col
                break
    
    if work_type_col is None:
        # If no suitable column, create empty plot
        fig = go.Figure()
    else:
        type_counts = df[work_type_col].value_counts()
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=type_counts.index,
            values=type_counts.values,
            hole=0.4,
            marker_colors=px.colors.sequential.Plasma
        ))
    
    fig.update_layout(
        title=dict(
            text=f'{work_type_col if work_type_col else "Category"} Distribution',
            font=dict(size=20, color='#2c3e50')
        ),
        template='plotly_white',
        showlegend=True,
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        font=dict(family="Arial, sans-serif", size=12, color="#2c3e50")
    )
    
    return fig.to_json()

def create_industry_distribution(df):
    """
    Create a bar chart for any industry-like column.
    """
    # Try to find an industry-like column
    industry_col = None
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].str.contains('industry|sector|business', case=False).any():
            industry_col = col
            break
    
    if industry_col is None:
        # If no industry column, use first categorical column
        for col in df.columns:
            if df[col].dtype == 'object':
                industry_col = col
                break
    
    if industry_col is None:
        # If no suitable column, create empty plot
        fig = go.Figure()
    else:
        industry_counts = df[industry_col].value_counts()
        
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=industry_counts.index,
            y=industry_counts.values,
            marker_color='#2c3e50'
        ))
    
    fig.update_layout(
        title=dict(
            text=f'{industry_col if industry_col else "Category"} Distribution',
            font=dict(size=20, color='#2c3e50')
        ),
        xaxis_title=industry_col if industry_col else 'Category',
        yaxis_title='Count',
        template='plotly_white',
        showlegend=False,
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        font=dict(family="Arial, sans-serif", size=12, color="#2c3e50")
    )
    
    return fig.to_json()

def create_company_size_distribution(df):
    """
    Create a pie chart for any size-like column.
    """
    # Try to find a size-like column
    size_col = None
    for col in df.columns:
        if df[col].dtype == 'object' and df[col].str.contains('size|employees|headcount', case=False).any():
            size_col = col
            break
    
    if size_col is None:
        # If no size column, use first categorical column
        for col in df.columns:
            if df[col].dtype == 'object':
                size_col = col
                break
    
    if size_col is None:
        # If no suitable column, create empty plot
        fig = go.Figure()
    else:
        size_counts = df[size_col].value_counts()
        
        fig = go.Figure()
        fig.add_trace(go.Pie(
            labels=size_counts.index,
            values=size_counts.values,
            hole=0.4,
            marker_colors=px.colors.sequential.Plasma
        ))
    
    fig.update_layout(
        title=dict(
            text=f'{size_col if size_col else "Category"} Distribution',
            font=dict(size=20, color='#2c3e50')
        ),
        template='plotly_white',
        showlegend=True,
        height=400,
        margin=dict(l=50, r=50, t=80, b=50),
        font=dict(family="Arial, sans-serif", size=12, color="#2c3e50")
    )
    
    return fig.to_json() 