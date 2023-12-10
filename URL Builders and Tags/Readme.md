## [URL Shortner](https://github.com/Hamzahmed/Work_Projects/tree/main/URL%20Shortner)/[Building Links](https://github.com/Hamzahmed/Work_Projects/tree/main/Building%20Links)
Our project involved assisting a large enterprise in tracking their health enrollment website and understanding visitor behavior. To track website metrics, we initially utilized Adobe Analytics. However, our client had specific requirements to track clicks separately and encountered limitations with using Bitly for URL shortening due to budget constraints, time consumption, and maximum URL restrictions.

To address these challenges and provide a faster and custom solution, I developed tools to meet our client's needs. The first tool was a URL shortener, where we generated shortened links that our clients could implement on their website. This allowed us to track clicks separately from Adobe Analytics and gather specific metrics tailored to our client's requirements. The URL shortener solution was built using Flask and Python, providing a flexible and efficient framework.

Additionally, our client requested another solution that retained the original URL name but added a CID (Campaign ID) at the end of the URL to make it trackable. This approach allowed us to maintain consistency with existing URLs while incorporating tracking capabilities. This solution, also developed using Flask, Python, and Docker containers, facilitated efficient tracking and data gathering.

To collect and store click data, I utilized SQLite3, a lightweight and embedded database management system. SQLite3 efficiently managed the storage of click data, ensuring that all relevant information was accurately captured and easily accessible for analysis.

The deployment and hosting of these solutions were streamlined using Docker containers. Docker provided a scalable and efficient environment for running the Flask applications, making it easy to manage and maintain the tools.

Through the implementation of these custom solutions, we successfully addressed our client's requirements for tracking website metrics and monitoring visitor behavior. The URL shortener and trackable URL solutions enabled us to gather valuable data, analyze click patterns, and generate insights into visitor interactions on the health enrollment website.

By leveraging Flask, Python, SQLite3, and Docker, we developed efficient and flexible tools that met our client's needs within the given constraints. These solutions exemplify our commitment to providing tailored and innovative solutions to track and analyze website metrics, empowering our clients to make informed decisions based on accurate data.
