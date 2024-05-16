from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from database import get_database_connection
from .scraper import scrape_quotes

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
