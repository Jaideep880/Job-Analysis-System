from flask import Flask, render_template, request, redirect, url_for, flash
import pandas as pd
import os
from datetime import datetime
from utils.visualizations import (
    create_trend_plot, create_forecast_plot, create_salary_distribution,
    create_skills_analysis, create_location_distribution, create_remote_vs_onsite,
    create_industry_distribution, create_company_size_distribution
)

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for flash messages

# Ensure the upload directory exists
UPLOAD_FOLDER = os.path.join('data', 'processed')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def index():
    # Load the job market data
    file_path = os.path.join(UPLOAD_FOLDER, 'job_market_data.csv')
    df = None
    total_jobs = 0
    avg_salary = 0
    remote_percentage = 0
    ai_adoption = 0
    
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
            if not df.empty:
                # Calculate summary statistics
                total_jobs = len(df)
                if 'salary' in df.columns:
                    avg_salary = round(df['salary'].mean() / 100000, 1)  # Convert to lakhs, round to 1 decimal
                if 'remote_friendly' in df.columns:
                    remote_percentage = round((df['remote_friendly'].str.lower() == 'remote').mean() * 100, 1)
                if 'ai_adoption_level' in df.columns:
                    ai_adoption = round((df['ai_adoption_level'].str.lower() == 'very high').mean() * 100, 1)
                
        except Exception as e:
            flash(f'Error loading data for homepage statistics: {str(e)}', 'error')
            
    return render_template('index.html',
                           total_jobs=total_jobs,
                           avg_salary=avg_salary,
                           remote_percentage=remote_percentage,
                           ai_adoption=ai_adoption)

@app.route('/upload', methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect(url_for('index'))
    
    if not file.filename.endswith('.csv'):
        flash('Please upload a CSV file', 'error')
        return redirect(url_for('index'))
    
    try:
        # Save the uploaded file
        file_path = os.path.join(UPLOAD_FOLDER, 'job_market_data.csv')
        file.save(file_path)
        
        # Read the CSV file
        df = pd.read_csv(file_path)
        
        # Basic validation - check if file is empty
        if df.empty:
            flash('The uploaded file is empty', 'error')
            return redirect(url_for('index'))
            
        # Check if there are at least some basic columns
        if len(df.columns) < 2:
            flash('The CSV file must have at least 2 columns', 'error')
            return redirect(url_for('index'))
            
        return redirect(url_for('dashboard'))
    except Exception as e:
        flash(f'Error processing file: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    # Load the job market data
    file_path = os.path.join(UPLOAD_FOLDER, 'job_market_data.csv')
    if not os.path.exists(file_path):
        flash('Please upload a CSV file first', 'error')
        return redirect(url_for('index'))
    
    try:
        df = pd.read_csv(file_path)
        
        # Calculate summary statistics based on available columns
        total_jobs = len(df)
        
        # Try to calculate average salary if a numeric column exists
        avg_salary = 0
        for col in df.columns:
            if df[col].dtype in ['int64', 'float64']:
                avg_salary = df[col].mean() / 100000  # Convert to lakhs
                break
        
        # Try to find remote work percentage if a text column contains 'remote'
        remote_percentage = 0
        for col in df.columns:
            if df[col].dtype == 'object':
                if df[col].str.lower().str.contains('remote').any():
                    remote_percentage = round((df[col].str.lower().str.contains('remote').mean() * 100), 1)
                    break
        
        # Try to find AI adoption if a text column contains 'ai' or 'artificial intelligence'
        ai_adoption = 0
        for col in df.columns:
            if df[col].dtype == 'object':
                if df[col].str.lower().str.contains('ai|artificial intelligence').any():
                    ai_adoption = round((df[col].str.lower().str.contains('ai|artificial intelligence').mean() * 100), 1)
                    break
        
        # Get current date
        current_date = datetime.now().strftime("%d %B %Y")
        
        # Create visualizations based on available data
        trend_plot = create_trend_plot(df)
        forecast_plot = create_forecast_plot(df)
        salary_plot = create_salary_distribution(df)
        skills_plot = create_skills_analysis(df)
        location_plot = create_location_distribution(df)
        remote_plot = create_remote_vs_onsite(df)
        industry_plot = create_industry_distribution(df)
        company_size_plot = create_company_size_distribution(df)
        
        return render_template('dashboard.html',
                             total_jobs=total_jobs,
                             avg_salary=avg_salary,
                             remote_percentage=remote_percentage,
                             ai_adoption=ai_adoption,
                             current_date=current_date,
                             trend_plot=trend_plot,
                             forecast_plot=forecast_plot,
                             salary_plot=salary_plot,
                             skills_plot=skills_plot,
                             location_plot=location_plot,
                             remote_plot=remote_plot,
                             industry_plot=industry_plot,
                             company_size_plot=company_size_plot)
    except Exception as e:
        flash(f'Error analyzing data: {str(e)}', 'error')
        return redirect(url_for('index'))

@app.route('/recommender')
def recommender():
    """
    Render the job recommender page.
    """
    return render_template('recommender.html', recommended_jobs=None)

@app.route('/recommend', methods=['POST'])
def recommend():
    """
    Process user input and display job recommendations.
    """
    user_skills_str = request.form.get('skills', '')
    user_experience = request.form.get('experience', '')
    
    # Load data
    file_path = os.path.join(UPLOAD_FOLDER, 'job_market_data.csv')
    df = pd.DataFrame() # Initialize with empty DataFrame
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            flash(f'Error loading data for recommendations: {str(e)}', 'error')
            return render_template('recommender.html', recommended_jobs=[])

    if df.empty:
        flash('No job data available for recommendations. Please upload data first.', 'warning')
        return render_template('recommender.html', recommended_jobs=[])

    # Call the recommendation logic (to be implemented)
    recommended_jobs = recommend_jobs(df, user_skills_str, user_experience)
    
    return render_template('recommender.html', recommended_jobs=recommended_jobs)

def recommend_jobs(df, skills_str, experience):
    """
    Placeholder for job recommendation logic.
    Filter jobs based on skills and experience.
    """
    # TODO: Implement actual recommendation logic
    # For now, return all jobs matching experience
    if experience:
        filtered_df = df[df['experience_level'].str.lower() == experience.lower()].copy()
    else:
        filtered_df = df.copy()
        
    # Dummy filtering by skills (exact match for demonstration)
    if skills_str:
        user_skills = [skill.strip().lower() for skill in skills_str.split(',') if skill.strip()]
        if user_skills:
            # Simple check: does the job's skills string contain any of the user's skills?
            # This needs more robust implementation for partial matches, skill variations, etc.
            filtered_df = filtered_df[filtered_df['skills'].str.lower().str.contains('|'.join(user_skills), na=False)]
            
    # Convert DataFrame rows to a list of dictionaries for easier handling in template
    return filtered_df.to_dict('records')

if __name__ == '__main__':
    app.run(debug=True) 