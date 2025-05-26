# Sales Data Analysis with Python
This project was developed by Rodrigo Dantas as part of his learning journey in data analysis and aims to simulate a business challenge using a sales dataset. The focus was on transforming raw data into actionable insights while applying industry-standard tools and techniques, including fundamental Machine Learning concepts for forecasting.

### Key Contributions:

- Data Integration & Cleaning: Designed and merged relational tables (customers, products, and orders) into a clean, analysis-ready dataset, ensuring data consistency and readiness for further processing.

- Feature Engineering: Applied date parsing and data cleaning to ensure consistency across time-based analyses. Engineered a Lucro (Profit) metric using custom logic that integrates sales values, discounts, and product/delivery costs, providing a comprehensive view of profitability.

- Exploratory Data Analysis (EDA): Identified sales trends over time, segmented performance by product pricing, and analyzed customer behavior to uncover key patterns and insights.

- Sales Forecasting with Machine Learning:
    - Utilized Scikit-Learn to build and interpret a Linear Regression model aimed at forecasting future sales behavior.
    - The model was trained on historical monthly sales data to predict sales trends, demonstrating the application of predictive analytics in a business context.
    - This forecasting component provides a forward-looking perspective, enabling potential strategic planning based on predicted sales volumes.

- Impact Analysis: Investigated how delivery time impacts profitability through correlation analysis, highlighting operational factors that influence financial outcomes.

- Data Visualization: Created compelling visualizations using Matplotlib and Seaborn, including heatmaps and trend lines, to effectively communicate complex data insights and support data storytelling.

Throughout the process, I prioritized code readability, a modular structure, and clarity in insights, ensuring the project is easy to understand and extend.

### Project Structure
This project follows a standard and organized directory structure to enhance readability, maintainability, and collaboration.

- data/: This directory stores all raw and processed data files (e.g., .csv files) used in the analysis.

- src/: This directory contains all the source code for the project, including Python scripts for data processing, analysis, and visualization.

- figures/: This directory is intended to store all generated plots, charts, and other visual outputs from the analysis.

- INSIGHTS.md: This file provides a detailed breakdown of the analytical insights derived from the data, complemented by strategic recommendations for business application.

### Dependencies

To run this project, you need to have Python installed. The required libraries can be installed using `pip` from the `requirements.txt` file:

```bash
pip install -r requirements.txt

The requirements.txt file contains the following libraries:

pandas
numpy
seaborn
matplotlib
scikit-learn
scipy


This structure ensures a clear separation of concerns, making it easier to navigate and understand the project's components.

### Technologies
Python | Pandas, Matplotlib, Seaborn, NumPy, SciPy, Scikit-Learn