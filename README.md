# Macaronesia Analyser
This project is a Flask application that interacts with Azure OpenAI and a MySQL database to process and analyze data.

The data comes from an archery league, with results in a PDF that we transform into JSON using Azure Form Recognizer, and then insert into a database.

With the data in a manageable format, we can perform a multitude of tasks. In this case, we use it to create custom queries and cross-reference new and old data.

By having the data structured in a MySQL database, we can leverage SQL's powerful querying capabilities to generate insights and reports. For example, we can:

- Track performance trends over time by comparing historical data with recent results.
- Identify top performers and underperformers based on various metrics.
- Generate detailed reports for individual archers or clubs.
- Cross-reference data to find correlations and patterns that might not be immediately obvious.

This flexibility allows us to make data-driven decisions and gain a deeper understanding of the archery league's dynamics.

Additionally, having the data in a database opens up possibilities for further integration with other tools and services, such as data visualization platforms, machine learning models, and more.

By using Azure OpenAI to generate SQL queries, we can automate complex data analysis tasks, making it easier to extract valuable insights without needing extensive SQL knowledge.

In summary, transforming the PDF data into a structured format and storing it in a database not only simplifies data management but also unlocks a wide range of analytical possibilities.

## Main Files

- **[app.py](app.py)**: Main file that starts the Flask server and defines the API routes.
- **[azureOpenAIClient.py](azureOpenAIClient.py)**: Client to interact with Azure OpenAI and generate SQL queries.
- **[mySqlClient.py](mySqlClient.py)**: Client to interact with the MySQL database.
- **[recognizer/](recognizer/)**: Contains scripts to process PDF and JSON files.
- **[Dockerfile.dockerfile](Dockerfile.dockerfile)**: Defines the Docker configuration for the project.
- **[requirements.txt](requirements.txt)**: List of project dependencies.
- **[schema.sql](schema.sql)**: MySQL database schema.

## Installation

1. Clone the repository:
    ```sh
    git clone <REPOSITORY_URL>
    cd <REPOSITORY_NAME>
    ```

2. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up the environment variables in a `.env` file:

## Transformation Flow

Initial Format: PDF

The initial format of the data is a PDF, usually consisting of 2 or more pages containing a table with the following data: name, club, 6 columns with points, the sum of the best three, and the total sum. For the application, we will omit the last two.With the PDF, you can start training your custom extraction model.

With the PDF in the `recognizer/pdf` folder, we can execute the Python script `main.py`. This script will call the Form Recognizer API, which returns a JSON with all detected data. From this JSON, we need to extract only the relevant data that matches our model.

> **Note**: Sometimes, the free tier of Azure Form Recognizer does not detect more than two pages at a time in a PDF. In these cases, you will need to split the PDF and send it in smaller parts.

At this point, we could insert the data into the database, but I prefer to keep a copy of the processed file to avoid reprocessing if needed. Therefore, we execute the script `saveInDatabase.py` or use the API endpoint `/api/process/json`. This will search for the files in `recognizer/json` in the database and insert them if they do not exist.

With this completed, we will have our PDF data in a MySQL database.


## Why Use Azure Form Recognizer

Azure Form Recognizer is a powerful and versatile tool that can significantly streamline the process of extracting data from documents. Depending on the size of your project, you can take advantage of the generous free tier, which offers ample usage for many applications.

### Key Benefits

- **Accuracy**: Form Recognizer uses advanced machine learning models to accurately extract text, key-value pairs, and tables from documents.
- **Efficiency**: Automates the data extraction process, reducing the time and effort required for manual data entry.
- **Scalability**: Easily scales to handle large volumes of documents, making it suitable for both small and large projects.
- **Integration**: Seamlessly integrates with other Azure services, such as Azure Storage and Azure Cognitive Services, to create a comprehensive data processing pipeline.
- **Customization**: Allows you to train custom models tailored to your specific document formats, improving extraction accuracy for specialized use cases.

