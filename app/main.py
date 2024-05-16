import csv
import os
from datetime import datetime

from fastapi import FastAPI, Response
from pydantic import BaseModel
from typing import List
from database import get_database_connection
from .scraper import scrape_quotes
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


class ScrapingData(BaseModel):
    text: str
    author: str


@app.get("/")
async def root():
    return {"Hello": "World"}


@app.post("/scrape_data")
async def create_user(scrapes: List[ScrapingData]):
    connection = get_database_connection()

    try:
        cursor = connection.cursor()

        for scrape in scrapes:
            data_to_insert = (scrape.text, scrape.author)
            cursor.execute('INSERT INTO scraping_data (text, author) VALUES (%s, %s)', data_to_insert)

        connection.commit()
        return {"message": "Data saved successfully"}
    except Exception as e:
        connection.rollback()
        raise e
    finally:
        cursor.close()
        connection.close()


@app.get("/scrapes")
async def read_users():
    connection = get_database_connection()
    cursor = connection.cursor()
    query = "SELECT * FROM scraping_data"
    cursor.execute(query)
    data = cursor.fetchall()
    connection.close()
    return data


@app.get("/get_web_scrape_data")
def get_web_scrape_data():
    return scrape_quotes()


@app.get("/export_csv")
async def export_csv(response: Response):
    try:
        connection = get_database_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM scraping_data")
        data = cursor.fetchall()

        download_folder = os.getenv("download_file_path")
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        csv_file_name = f"scraping_data_{timestamp}.csv"
        csv_file_path = os.path.join(download_folder, csv_file_name)

        with open(csv_file_path, mode="w", newline="") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow([i[0] for i in cursor.description])
            csv_writer.writerows(data)

        response.headers["Content-Disposition"] = f"attachment; filename={csv_file_name}"
        response.headers["Content-Type"] = "text/csv"

        with open(csv_file_path, mode="r") as csv_file:
            csv_content = csv_file.read()

        return Response(content=csv_content, media_type="text/csv")
    finally:
        cursor.close()
        connection.close()