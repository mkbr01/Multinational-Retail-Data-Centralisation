# Multinational-Retail-Data-Centralisation

Project Title
Multinational Retail Data Centralisation


Project Overview
The goal of the Data Centralisation Project is to gather, refine, and merge data from various origins into a single PostgreSQL database. This project tackles the issue encountered by a multinational retailer with dispersed data, which complicates accessibility and analysis. By centralising the data, the project streamlines information handling, maintains data uniformity, and offers a holistic perspective on the company’s activities.


**Project Dependencies and Requirements
**
Python Libraries:
pandas
numpy
sqlalchemy
psycopg2
tabula
requests
boto3
yaml
AWS Credentials:

Ensure that AWS access key ID and secret access key are properly configured in the environment variables. These credentials are necessary for accessing S3 buckets.
Database Credentials YAML File:

Create a YAML file named db_creds.yaml with the following structure:

yaml
RDS_DATABASE_TYPE: "postgresql"
DB_API: "psycopg2"
RDS_USER: "<RDS_USERNAME>"
RDS_PASSWORD: "<RDS_PASSWORD>"
RDS_HOST: "<RDS_HOSTNAME>"
RDS_PORT: "<RDS_PORT>"
RDS_DATABASE: "<RDS_DATABASE_NAME>"
LOCAL_DATABASE_TYPE: "postgresql"
LOCAL_DB_API: "psycopg2"
LOCAL_USER: "<LOCAL_DB_USERNAME>"
LOCAL_PASSWORD: "<LOCAL_DB_PASSWORD>"
LOCAL_HOST: "<LOCAL_DB_HOST>"
LOCAL_PORT: "<LOCAL_DB_PORT>"
LOCAL_DATABASE: "<LOCAL_DATABASE_NAME>"


**Installation**

Step 1: Clone the Repository
Clone the repository using Git:

bash
git clone https://github.com/mkbr01/Multinational-Retail-Data-Centralisation.git
Step 2: Setup the Environment
Create a virtual environment and install dependencies:

bash
cd multinational-retail-data-centralisation
python3 -m venv venv
source venv/bin/activate
pip install pandas numpy sqlalchemy psycopg2 tabula requests boto3 pyyaml

**Usage
**
Credentials
Ensure PostgreSQL and AWS credentials are set up in YAML files.

Executing the Data Centralisation
Run the provided script to start the data centralisation process:

bash
./run-scripts.sh



### Milestones

1. **Data Extraction and Cleaning:** Extracted data from various sources, including RDS Tables, PDFs, APIs, and AWS S3 Buckets. Implemented thorough data cleaning processes to ensure accuracy and consistency.
2. **Data Wrangling and Formatting with PostgreSQL:** Ensured data were stored in correct types within tables. Tasks included determining maximum character limits for VARCHAR data and updating tables accordingly.
3. **Developed Star-Based Schema:** Established the star-based schema of the database, ensuring columns adhered to correct data types.
4. **Data Querying:** Formulated business-related questions and extracted data from the database using SQL queries.



### Project Conclusion

The Multinational Retail Data Centralisation project successfully centralized retail data from multiple multinational retail entities into a unified PostgreSQL database. Key accomplishments include:

Data Extraction: Utilized various methods to extract data from relational databases, PDF files, and S3 buckets.

Data Cleaning: Implemented robust procedures to ensure data quality, including handling missing values, standardizing formats, and converting units.

Data Loading: Uploaded cleaned data into PostgreSQL, organizing it into appropriate tables for efficient storage and retrieval.

Process Automation: Developed scripts for automating the data centralization process, improving efficiency and reproducibility.
