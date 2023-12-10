## [Social Media Dashboard](https://github.com/Hamzahmed/Work_Projects/tree/main/Social%20Media%20Dashboard)
As the lead responsible for integrating data from various sources across multiple business functions, I spearheaded the creation of automated tools to streamline this process. These tools played a crucial role in connecting and gathering data from five distinct APIs. The aggregated data was then stored in a centralized data warehouse powered by Snowflake.

The Snowflake data warehouse served as the foundation for generating insightful reports and visualizations through Tableau and Looker dashboards. By consolidating data from disparate sources, we enabled comprehensive analytics and reporting capabilities that supported data-driven decision-making across the organization.

In addition to data integration and reporting, I also took the initiative to implement Machine Learning algorithms for sentiment analysis. This involved leveraging the acquired social media data from the API connections and applying advanced algorithms to analyze and extract sentiment-related insights. By incorporating sentiment analysis into our reports, we provided a deeper understanding of customer sentiment and opinions, facilitating quicker and more informed decision-making processes.

The inclusion of Machine Learning algorithms in our reports added a layer of intelligence to our analytics efforts. These algorithms helped identify trends, sentiment patterns, and emerging insights from the social media data, enabling stakeholders to make smarter decisions based on real-time information.

By integrating data from multiple sources, establishing a robust data warehouse on Snowflake, and incorporating Machine Learning algorithms for sentiment analysis, our team successfully created a data-driven ecosystem. This ecosystem empowered the organization with accurate, timely, and actionable insights, facilitating informed decision-making and driving positive outcomes across various business functions.

### [SproutSocial_GoogleSheet_Snowflake](https://github.com/Hamzahmed/Work_Projects/tree/main/Social%20Media%20Dashboard/SproutSocial_GoogleSheet_Snowflake)

The primary objective of this project was to develop a comprehensive dashboard that would provide our client with real-time social media metrics, enabling them to make informed decisions promptly. To achieve this, we utilized a combination of ELT tools, APIs, and data warehousing techniques.

Our data integration process was facilitated by Fivetran, an ELT (Extract, Load, Transform) tool. We connected and extracted data from multiple sources, including Google Analytics, YouTube Analytics, Google Ads, and Facebook Ads. The extracted data was then transformed and loaded into a data warehouse created on Snowflake, a cloud-based data platform known for its scalability and performance.

In addition to the above-mentioned platforms, we also leveraged Sprout Social, a social media management platform, to streamline our social media efforts. Sprout Social provided us with a unified platform to manage and analyze social media activities across LinkedIn, Twitter, Facebook, and Instagram. By utilizing the Sprout Social API, we seamlessly integrated the social media data into our Snowflake data warehouse.

Our focus was on tracking the performance and engagement of social media posts, which included metrics such as impressions, engagements, and clicks. We also aimed to gain insights into the overall health of social media profiles, monitoring factors like follower growth, follower churn, and competitor comparison.

To visualize and present the social media metrics and insights, we utilized Tableau, a powerful data visualization tool. The data from the Snowflake data warehouse powered the dashboards on Tableau, providing our client with up-to-date information on the performance and health of their social media profiles. These dashboards facilitated data-driven decision-making by highlighting trends, identifying areas for improvement, and allowing for quick assessments of social media performance.

By integrating data from multiple sources, including Google Analytics, YouTube Analytics, Google Ads, Facebook Ads, and Sprout Social, we created a comprehensive and dynamic social media dashboard. This dashboard empowered our client to monitor and optimize their social media presence, gain actionable insights, and make informed decisions to drive their social media strategy forward.

### [Youtube_Snowflake](https://github.com/Hamzahmed/Work_Projects/tree/main/Social%20Media%20Dashboard/Youtube_Snowflake)

During the project, we encountered a limitation with the Fivetran ELT connection for YouTube Analytics. Specifically, the connection only provided us with the video IDs and not the corresponding video titles. As a result, we needed to find a solution to retrieve the missing video titles while adhering to budget constraints that prevented us from utilizing additional software such as Social Blade.

To address this challenge, we devised a free, albeit slightly heavier solution. We leveraged the data stored in Snowflake, our data warehouse, by extracting the YouTube Analytics table into our script and converting it into a dataframe. Although the table contained only the video IDs, this served as a starting point for retrieving the video titles.

To obtain the video titles, we converted the video IDs into URLs using the YouTube domain. By constructing the appropriate URLs, we were able to scrape the video titles directly from the YouTube website. This process involved querying the YouTube website using the URLs and extracting the corresponding video titles.

Once we retrieved the video titles, we appended them back into the dataframe, ensuring that we had the complete dataset with both video IDs and their respective titles. This allowed us to have a comprehensive and accurate representation of the YouTube video metrics in our database.

While this solution required additional processing steps and the use of web scraping techniques, it provided a cost-effective approach to retrieve the missing video titles without relying on external software. By leveraging the data available in our Snowflake data warehouse and utilizing web scraping within our script, we successfully enriched our dataset with the video titles, enabling a more comprehensive analysis of the YouTube video metrics.

This solution showcases our resourcefulness in finding creative and efficient ways to overcome limitations and ensure the completeness and accuracy of the data we worked with.