## [QA Automation](https://github.com/Hamzahmed/Work_Projects/tree/main/QA%20Automation)
Our client tasked us with validating the data flow from SQL Servers to their AWS environment. The data was in the form of XML files stored as columns within the SQL Server tables. To validate this data, we needed to parse the XML files and convert them into respective tables based on the dataset. 

To achieve this, we utilized the native AWS Athena XML parser to parse the XML files and generate the corresponding tables. However, to ensure the accuracy and validity of the parsed tables, manual validation by an individual engineer was required.

To streamline and automate the data validation process, I created a Glue Job specifically designed for validating the data loads between the SQL Server tables in Athena and the XML tables in SQL Server.

Within the ETL job, I first defined the necessary parameters to be passed through the job. In the case of the policyID job, these parameters could either be a list provided in CSV format or manually entered. These policy IDs were crucial for identifying and retrieving the relevant rows from both the Athena and SQL Server tables.

After retrieving the rows based on the defined policy IDs, I implemented a validation process to compare the data between the Athena and SQL Server tables. This involved validating the versions, timestamps, and any updates between the two tables. By performing these checks, we ensured data consistency and integrity throughout the migration process.

The XML validation aspect was more complex. To accomplish this, I utilized the Python native library ElementTree. Rather than using a package to parse through the XML directly, I broke down the XML files into "blocks" and validated individual lines within those blocks to perform accurate data comparisons. If the data existed in both the XML block and the corresponding Athena table, a boolean value of 'True' was in the row value of the Athena table. However, if a mismatch was found between the XML block and the Athena table, a boolean value of 'False' was recorded, along with the specific data point in the XML where the discrepancy occurred.

By implementing this comprehensive data validation process, we ensured the accuracy and reliability of the data during the migration from SQL Servers to the AWS environment. Our solution combined automation through Glue Jobs, manual validation checks, and customized XML validation techniques, all aimed at guaranteeing the integrity of the migrated data.
