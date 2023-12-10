## [AWS Optimization](https://github.com/Hamzahmed/Work_Projects/tree/main/AWS%20Optimization)

Our team was tasked with validating and implementing AWS Glue ETL scripts for our client, who was in the process of migrating their database from SQL Server to AWS. Additionally, we took on the responsibility of optimizing their AWS Redshift database and Athena tables, with a particular focus on enhancing the efficiency and productivity of the tables.

In regards to the Athena tables, we employed several optimization techniques. Firstly, we applied partitioning to the tables. Partitioning is a practice that involves dividing the data into logical segments based on specific criteria, such as time. By partitioning the tables based on the year column, we restricted the amount of data scanned by each query, leading to improved query performance and reduced costs. To achieve this, we converted the time-based column from a string type to a timestamp and extracted the year data into a separate column. We then partitioned the table based on the year column and further optimized it by bucketing the data using unique IDs.

We carefully designed the partitioning scheme, creating six partitions based on the years 2012, 2013, 2014, 2018, 2020, and 2021. These partitions were bucketed using the 95 distinct unique IDs. By implementing this partitioning strategy, we observed a significant reduction in the amount of data scanned by queries, resulting in improved query performance. Specifically, we observed a 25% decrease in total data scanned, with the compressed data size reduced from 3.08 MB to 2.30 MB for both queries.

In addition to partitioning, we leveraged GZIP compression to further optimize the Athena tables. By compressing the data using GZIP, we were able to significantly reduce the data size scanned during queries. This optimization resulted in a reduction in the scanned data from 3.47 MB to 2.30 MB, further lowering costs. It's important to note that Athena charges based on the size of data scanned, so this compression technique led to cost savings for our client.

By implementing partitioning and GZIP compression techniques, we not only improved the performance and efficiency of the Athena tables but also contributed to reducing the overall costs associated with data scanning. Our efforts demonstrate our commitment to optimizing our client's AWS ecosystem, ensuring that their data operations are streamlined and cost-effective.

### Stack
AWS Redshift
\
AWS Athena
\
S3 Storage Buckets
\
SQL
\
XML
