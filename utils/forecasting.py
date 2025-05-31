import pandas as pd
from prophet import Prophet
import plotly.graph_objects as go

def generate_forecast(df, periods=12):
    """
    Generate job posting forecast using Prophet.
    
    Args:
        df (pd.DataFrame): Job market data
        periods (int): Number of months to forecast
    
    Returns:
        str: JSON string of the forecast plot
    """
    # Prepare data for Prophet
    df['year_month'] = df['published_date'].dt.to_period('M')
    monthly_counts = df.groupby('year_month').size().reset_index(name='count')
    monthly_counts['year_month'] = monthly_counts['year_month'].astype(str)
    
    prophet_df = pd.DataFrame({
        'ds': pd.to_datetime(monthly_counts['year_month']),
        'y': monthly_counts['count']
    })
    
    # Initialize and fit Prophet model
    model = Prophet(yearly_seasonality=True, weekly_seasonality=False)
    model.fit(prophet_df)
    
    # Create future dataframe and make predictions
    future = model.make_future_dataframe(periods=periods, freq='M')
    forecast = model.predict(future)
    
    # Create plot
    fig = go.Figure()
    
    # Add actual data
    fig.add_trace(go.Scatter(
        x=prophet_df['ds'],
        y=prophet_df['y'],
        name='Actual',
        line=dict(color='royalblue')
    ))
    
    # Add forecast
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat'],
        name='Forecast',
        line=dict(color='red')
    ))
    
    # Add confidence intervals
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat_upper'],
        fill=None,
        mode='lines',
        line_color='rgba(255,0,0,0.1)',
        name='Upper Bound'
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast['ds'],
        y=forecast['yhat_lower'],
        fill='tonexty',
        mode='lines',
        line_color='rgba(255,0,0,0.1)',
        name='Lower Bound'
    ))
    
    fig.update_layout(
        title='Job Postings Forecast',
        xaxis_title='Date',
        yaxis_title='Number of Job Postings',
        width=800,
        height=600
    )
    
    return fig.to_json() 