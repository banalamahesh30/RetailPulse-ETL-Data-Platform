# RetailPulse ETL Data Platform — Setup Guide

## Introduction

RetailPulse ETL Data Platform is an end-to-end e-commerce Data Engineering project designed to demonstrate how raw transactional data can be extracted, transformed, validated, stored in a cloud data warehouse, analyzed using SQL, and visualized through interactive business dashboards.

The project processes more than **6.8 million source records** across customers, products, sellers, warehouses, orders, order items, payments, shipments, returns, and reviews.

## Technology Stack

The project is developed using the following technologies:

- **MySQL** — Source database
- **Python** — Data extraction and ETL processing
- **Pandas** — Data handling and file processing
- **Databricks** — Transformation environment
- **PySpark** — Large-scale data cleaning and transformation
- **Parquet** — Optimized data storage format
- **Snowflake** — Cloud data warehouse
- **SQL** — Data analysis and analytical queries
- **Power BI** — Business intelligence and visualization
- **Git & GitHub** — Version control and project portfolio
- **VS Code** — Development environment

## Environment Setup

Before running the project, Python, MySQL, Git, VS Code, Databricks, Snowflake, and Power BI Desktop must be installed and configured.

The required Python dependencies are maintained in the `requirements.txt` file.

Database credentials and environment-specific configuration are stored securely in a `.env` file. The `.env` file is excluded from GitHub to prevent sensitive MySQL and Snowflake credentials from being exposed.

## Source Database Setup

MySQL is used as the source database for the project.

The source database is:

**RETAIL_SOURCE_DB**

It contains the following ten e-commerce tables:

- Customers
- Products
- Sellers
- Warehouses
- Orders
- Order Items
- Payments
- Shipments
- Returns
- Reviews

These tables represent the transactional source layer of the RetailPulse platform.

## Data Extraction

Python is used to connect to MySQL and extract data from each source table.

Separate extraction modules are maintained for customers, products, sellers, warehouses, orders, order items, payments, shipments, returns, and reviews.

The project also contains an `extract_all.py` module to coordinate the extraction process.

Extracted data is stored inside the `data/raw/` directory in both **CSV and Parquet formats**.

This raw layer preserves the extracted source data before transformation.

## Data Transformation

The extracted datasets are processed using **Databricks and PySpark**.

The transformation process includes:

- Duplicate detection and removal
- NULL-value validation
- Data-type conversion
- Date standardization
- Text cleaning
- Whitespace trimming
- Hidden-character removal
- Categorical-value standardization
- Invalid-value detection
- Primary-key validation
- Foreign-key validation
- Business-rule validation
- Record-count validation

After cleaning and validation, the transformed datasets are stored in Parquet format under the `data/Transformed/` layer.

## Data Warehouse Preparation

After transformation, analytics-ready dimension and fact datasets are prepared.

The dimension layer contains:

- DIM_CUSTOMER
- DIM_DATE
- DIM_PRODUCT
- DIM_SELLER
- DIM_WAREHOUSE

The fact layer contains:

- FACT_SALES
- FACT_PAYMENTS
- FACT_SHIPMENTS
- FACT_RETURNS
- FACT_REVIEWS

This dimensional model separates descriptive business information from measurable transactional events and prepares the data for analytical workloads.

## Snowflake Data Warehouse

Snowflake is used as the cloud analytical warehouse.

The transformed dimension and fact datasets are loaded into Snowflake using dedicated Python loading modules.

The Snowflake layer provides centralized, analytics-ready data that can be queried using SQL and consumed by Power BI.

Analytical views are also created to simplify common business analysis and reporting requirements.

## ETL Pipeline

The project contains a central `run_pipeline.py` module for coordinating the ETL workflow.

The ETL framework is supported by dedicated modules for:

- MySQL connectivity
- Snowflake connectivity
- Configuration management
- Logging
- Error handling
- Data extraction
- Data loading
- Data validation

Pipeline execution information is written to the project log files, making it easier to identify successful stages and troubleshoot failures.

## Logging and Error Handling

Logging is implemented to track important ETL activities and pipeline execution.

The primary pipeline log is stored in:

**logs/etl_pipeline.log**

A dedicated error-handling module is used to capture and manage failures during pipeline execution.

This improves the reliability, maintainability, and traceability of the ETL workflow.

## Testing and Validation

Data validation is performed throughout the project to ensure the reliability of the pipeline.

The testing process includes:

- Source record-count validation
- Transformed record-count validation
- Snowflake record-count validation
- Duplicate validation
- NULL validation
- Transformation validation
- Primary-key validation
- Foreign-key validation
- End-to-end ETL testing
- Performance checking
- Documentation of issues and fixes

Additional validation utilities are included in the project to verify Snowflake tables and loaded warehouse data.

## SQL Analytics

Once the warehouse data is available in Snowflake, SQL is used to perform business analysis.

The analytical layer includes:

- Sales analysis
- Customer analysis
- Product analysis
- Seller analysis
- Payment analysis
- Shipment analysis
- Return analysis
- Review analysis
- Monthly trend analysis
- Executive KPI analysis

Advanced SQL concepts such as JOINs, CTEs, window functions, ranking functions, running totals, moving averages, customer retention, and Customer Lifetime Value are used for deeper analysis.

## Power BI Reporting

Power BI is connected to the analytical data layer to create interactive business dashboards.

The project includes dashboards for:

- Executive Analysis
- Sales Analysis
- Customer Analysis
- Product Analysis
- Operation Analysis

The dashboards contain Card(new), charts,  slicers, trends, and other business visuals to convert warehouse data into meaningful insights.

## End-to-End Data Flow

The complete RetailPulse pipeline follows:

**MySQL → Python Extraction → Raw CSV/Parquet → Databricks/PySpark → Data Cleaning & Transformation → Transformed Parquet → Dimension & Fact Layer → Snowflake → SQL Analytics → Power BI**

## Security

Sensitive information such as database usernames, passwords, Snowflake account information, and other credentials must not be stored directly in source code or committed to GitHub.

Environment-specific credentials are maintained through the `.env` file, which should always remain excluded through `.gitignore`.

## Conclusion

The RetailPulse ETL Data Platform demonstrates a complete Data Engineering and Analytics workflow, starting from a relational source database and ending with interactive business dashboards.

The project demonstrates practical experience with **MySQL, Python, PySpark, Databricks, Snowflake, SQL, Power BI, dimensional modeling, ETL development, data-quality validation, logging, error handling, and end-to-end pipeline testing**.