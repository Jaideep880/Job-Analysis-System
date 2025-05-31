# Job Market Analysis Dashboard

This project is a web application built with Flask to analyze and visualize job market data.

## Features

- Upload CSV job data.
- Display key job market statistics (Total Jobs, Average CTC, Remote Opportunities, AI/ML Roles).
- Visualize job market trends over time.
- Display distributions for salary, skills, location, work type, industry, and company size.
- Simple job market forecasting.

## Setup

1.  **Clone the repository (if applicable) or ensure you have the project files.**

2.  **Navigate to the project directory.**

    ```bash
    cd PROJECT
    ```

3.  **Navigate into the application directory.**

    ```bash
    cd job_market_app
    ```

4.  **Install the required dependencies.** Make sure you have Python installed (version 3.6 or higher recommended).

    ```bash
    pip install -r requirements.txt
    ```

## Running the Application

1.  **Navigate to the `job_market_app` directory** if you are not already there.

    ```bash
    cd job_market_app
    ```

2.  **Run the Flask application.**

    ```bash
    python app.py
    ```

3.  Open your web browser and go to `http://127.0.0.1:5000/` to access the application.

## Project Structure

```
PROJECT/
├── job_market_app/
│   ├── data/
│   │   └── processed/
│   │       └── job_market_data.csv (Uploaded/Processed data)
│   │   ├── static/
│   │   │   └── css/
│   │   │   └── style.css (Custom CSS)
│   │   ├── templates/
│   │   │   ├── base.html (Base template)
│   │   │   ├── dashboard.html (Dashboard page)
│   │   │   ├── error.html (Error page)
│   │   │   └── index.html (Homepage)
│   │   ├── utils/
│   │   │   ├── __init__.py
│   │   │   ├── data_loader.py (Data loading utility - *Note: Current implementation loads directly in app.py*)
│   │   │   ├── forecasting.py (Forecasting utility - *Note: Simple moving average implemented in visualizations.py*)
│   │   │   └── visualizations.py (Plotting utility)
│   │   ├── app.py (Flask application)
│   │   └── requirements.txt (Python dependencies)
│   └── README.md (This file)
```

## Project Overview for Data Analysts

This Flask-based web application serves as a powerful tool for data analysts to explore, visualize, and gain insights into job market trends. Its primary goal is to transform raw job posting data (in CSV format) into an interactive dashboard, making complex information easily digestible for decision-making or reporting.

**Key Components and Value for a Data Analyst:**

1.  **Data Ingestion (`/upload` route):**
    *   Analysts can easily upload a CSV file containing job market data.
    *   The application includes basic validation to ensure the presence of crucial columns (`title`, `published_date`, `salary`, etc.), which is vital for maintaining data quality and ensuring downstream analysis runs smoothly.
    *   The uploaded data is stored in a designated `data/processed` directory, providing a central location for the analytical source data.

2.  **Core Data Processing and Metrics (`app.py` & `utils/data_loader.py` - *although currently integrated*):**
    *   The application reads the CSV data using the powerful Pandas library, which is a standard tool in data analysis workflows for data manipulation and analysis.
    *   It calculates essential summary statistics directly from the loaded data:
        *   **Total Job Postings:** A fundamental metric indicating the volume of opportunities.
        *   **Average CTC (Cost To Company):** Provides a central tendency measure for compensation, crucial for salary benchmarking.
        *   **Remote Opportunities Percentage:** Gives insight into the prevalence of remote work based on the data provided (now correctly identifying 'Remote' entries).
        *   **AI/ML Roles Percentage:** Identifies the proportion of roles related to AI/ML based on the 'ai_adoption_level', highlighting a key area of market focus.

3.  **Advanced Visualization Suite (`utils/visualizations.py`):**
    *   Leveraging Plotly, the application generates a variety of interactive visualizations, allowing analysts to explore different facets of the job market:
        *   **Job Market Trends:** Tracks the volume of job postings over time (aggregated monthly), helping identify growth phases, seasonality, or declines.
        *   **Job Market Forecast:** Provides a simple forecast based on historical trends (currently using a moving average), offering a projection of future job posting volume.
        *   **Salary Distribution:** Visualizes the frequency of different salary ranges, helping understand typical compensation brackets.
        *   **Skills Analysis:** Highlights the most frequently mentioned skills, indicating current market demand.
        *   **Location Distribution:** Shows where the majority of job opportunities are located.
        *   **Work Location Distribution (Remote vs On-site/Hybrid):** A pie chart illustrating the breakdown of work arrangements.
        *   **Industry Distribution:** Displays which industries are posting the most jobs.
        *   **Company Size Distribution:** Breaks down job postings by company size, offering insights into opportunities across different organizational scales.
    *   These visualizations are presented on a single dashboard (`dashboard.html`), providing a holistic view of the job market landscape at a glance.

4.  **Technology Stack:**
    *   Built with **Flask**, a lightweight Python web framework, making it easy to understand and extend for Python-proficient data analysts.
    *   Relies heavily on **Pandas** for data handling and **Plotly** for generating interactive graphs, both standard libraries in the data science and analysis ecosystem.

In essence, this project provides a ready-to-use framework for a data analyst to quickly process, analyze, and visualize job market data from a CSV source, offering valuable insights into trends, distributions, and key metrics without requiring extensive coding for each analysis task.

## Data Format

The application expects a CSV file with the following columns:

- `title`
- `published_date` (in YYYY-MM-DD format)
- `salary`
- `location`
- `company`
- `description`
- `experience_level`
- `skills`
- `industry`
- `company_size`
- `ai_adoption_level`
- `automation_risk`
- `remote_friendly` (`Remote`, `Hybrid`, or other)
- `job_growth_projection`

A sample file structure is available at `job_market_app/data/processed/job_market_data.csv` after the first data upload or if you manually add one.

## Contributing

Feel free to fork the repository and contribute.

