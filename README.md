# Web Scraping and Data Export Project

This project is aimed at scraping quotes from a website and exporting them to a CSV file. It provides a FastAPI interface to interact with the scraping functionality and export the data.

## Installation

1. Clone this repository to your local machine.
2. Install the required dependencies using pip:
 pip install -m requirements.txt

## Usage

1. Make sure you have a MySQL database set up. Update the `.env` file with your database credentials.
2. Run the FastAPI server using the following command:

3. Open your web browser and go to `http://localhost:8000` to access the FastAPI documentation and API endpoints.

## API Endpoints

- **GET /**: Hello World message.
- **POST /scrape_data**: Scrapes quotes from the website and saves them to the database.
- **GET /scrapes**: Retrieves all scraped data from the database.
- **GET /get_web_scrape_data**: Scrapes quotes from the website and returns them as JSON.
- **GET /export_csv**: Exports the scraped data to a CSV file.