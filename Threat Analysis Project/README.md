ETL Pipeline Project
==============
# ETL Service Pipeline
This repository houses an ETL (Extract, Transform, Load) pipeline designed to fetch data from an online repository and seamlessly integrate it into a PostGIS database. The pipeline operates in a serverless environment, ensuring efficiency and scalability.
## Prototypes.py
I included this script just to show my ways of working. I usually work on Jupyter notebooks to test out connections and test out, experiment data, test joins and basically get an idea of how the ETL pipeline would work. Once it is all done, I make a .py file and just add everything nice and clean.
## environment and deployment
I have prepared a dockerfile to deploy the ETL Service and it will connect to the postgres database based on the environement variables. For secret handling, on the local environment I was just using environment variables, but I was using Actions to deploy the secrets as environment variables.  This is pretty much a standard of how I work with ETL pipelines, with the proper image, installations and secret handling. 
## How long did it take
It took about 3.5-4 hrs from conception to completion. I already have a standard process for deploying and configuring the environment and setting it up for Python scripts and Postgres  wasn't that difficult (30-45 mins). I took some time to study spatial joins (10-15 mins), but it wasn't really hard to understand at all because I am very confident in my pandas skills (have been using it for about 6 years now). Understanding the data and coming up with a pipeline design took the longest (1-1.5 hrs) because it required a lot of testing, POC and trial and errors.  Once that was done I was able to pretty much build the entire thing. Building the Pipeline (30 - 45 mins) with setting up, cleaning and deploying it into Postgres. For AI implementation, I just wanted to test the data and see how far I can go (20-30 mins)
---
# Methodology
## create_database.py
This script is responsible for creating a database and incorporating any desired extensions. In this case, we are leveraging PostGIS as our extension to tailor it to our specific use case.
## existing_data_into_postgres.py
This script facilitates the insertion of pre-existing data into PostgreSQL. Its primary function is to move data already residing in PostgreSQL into the specified table.
## ETL_Service.py
This script orchestrates the entire ETL process by invoking the previously mentioned scripts. It starts by creating a database, adding existing data into Postgres as 'eventdata' table, simulating an environment where data already exists. Subsequently, it retrieves the 'EventData' dataset from the 'threatanalysis' database.
The ETL process then involves acquiring 'county_data' as a GeoDataFrame named 'county_gdf' from a specified URL. Additionally, it fetches 'new_data' from 2021 to the present as another GeoDataFrame named 'gdf'. The goal is to spatially join the two datasets and then insert into the eventdata table. The gdf has lat/lon columns, and we will use Point from the shapely.geometry module to convert the lat/lon into Point geometry. After that we will do some pre-processing, changing the date column to datetime dtypes, handle None values and limit the data to only 2021. Then we finanlly do a spatial join between country_gdf and gdf. Once the data is joined, we will start to plan out to mirror the schema of the existing data. To do this, we will consolidate all the sources into one column called 'event_source', and then rename all the columns as the columns of the eventdata table. 
Next we aggregate the dataset and group it by event_id, event_date and geometry. Now we start the process of loading the data into the eventdata table in the database. Basically, I get the max of event_id and id in the eventdata table, and then I start the new dataset with that max+1. This way we are consistent with the uniquiness of event_id. 
---
# Improvements
Given more time, improvements to the process could include adding a timestamp to track when data is moved into the database, ensuring consistency in the ETL process and aiding users querying the dataset. Implementing incremental loading through methods like Change Data Capture (CDC) or time-based increments could enhance data quality, performance, reduce computational overhead, and preserve historical data.
Another suggestion is to incorporate validation checkpoints, unit/integration testing in the CI/CD pipeline, and embrace a data lake architecture with Landing, Raw, Refined, and Presentation layers for better data management and utilization.
The ETL pipeline will bring the data into the Landing layer, and then from Landing the data will be moved into Raw where the data can be processed and cleaned up. Once the data is processed, we will move the data into Refined layer where the data resides as tables that are ready to be deployed. Presentation layers is where you can make more tables on top of the cleaned up refined tables, to find more insights and implementation of the data.
---
# AI Implementations
I was curious to see if we can plug in this data into a query engine for an LLM. I made a rough draft just to test it out, but I didn't wanted to spend too much time on this. I'd have to think about the adequate embedding model for this dataset, and maybe decide what could be a good vector store. I used chromadb as the vector database, and langchain's GeoDataFrameLoader to prepare the data for embeddings. This is where I tested out some embeddings and used OpenAI's OpenAIEmbeddings to test out. It didn't really work that well honestly but I'd experiment it with a little more.
Note: The GeoDataFrameLoader is still in its very early stage. I noticed a bug in their package and I have merged my commit for review to their open source library. 
---
# Additional Considerations
It is crucial to address unconscious biases, especially when dealing with sensitive data, and reduce misinformation. Data engineers play a vital role in validating and researching data sources to confirm their reliability for specific use cases. The responsibility lies in providing data analysts with the most accurate and valid data possible.
Consideration of cloud-based solutions such as AWS Glue, AWS Lambdas, and Cloud Functions for automated deployment of ETL pipelines is recommended due to their robust, serverless, and scalable nature.
---