## [Podcast Data](https://github.com/Hamzahmed/Work_Projects/tree/main/Podcast%20Data)
The objective of this project was to create a robust database to support an ad campaign that encompassed multiple podcasts. This database served as the backbone for generating Looker Studio dashboards and reports, which were then made available on Google Sheets.

To accomplish this task, I developed a script that would retrieve all the relevant podcast data from a platform called Podsight. Podsight is a tracking tool specifically designed to monitor ad campaigns across various podcasts. The script collected the necessary data, ensuring that the client had access to up-to-date information on their podcast ads and could gain valuable insights from it.

To execute the project efficiently, I leveraged Python scripts in conjunction with Airflow running on a Docker container. We scheduled the scripts to run on a weekly basis, specifically every Monday and Wednesday. By automating the data retrieval process, we ensured that the latest podcast ad campaign information was consistently obtained.

Upon retrieving the data through the Podsight API, I organized it into a Pandas dataframe. This allowed for easy manipulation and calculation of various fields required for the ad campaign report. Additionally, I performed data cleaning procedures to ensure accuracy and consistency.

Once the necessary calculations and data cleanup were completed, I published the prepared data to a Google Sheet. This enabled a marketing analyst to access and utilize the report for further analysis and decision-making. By providing the data in an easily accessible format, we ensured seamless collaboration and facilitated data-driven insights for the client's ad campaign.

By deploying this systematic approach, we successfully established a comprehensive database, leveraging the Podsight API, Python scripts, Airflow, Docker, and Google Sheets. The automation of data retrieval, calculations, and publishing enabled efficient data management and empowered the client with actionable insights for their podcast ad campaigns.