from typing import Counter
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.logger import logger as fastapi_logger
import uvicorn, psycopg2, os, logging

# setup loggers
logging.config.fileConfig('logging.conf', disable_existing_loggers=False)

# get root logger
logger = logging.getLogger(__name__)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

db_user  = os.getenv('DB_USER')
db_pass  = os.getenv('DB_PASS')
db_port  = os.getenv('DB_PORT')
db_host  = os.getenv('DB_HOST')
db_db    = os.getenv('DB_DB')
hostname = os.getenv('HOSTNAME')

@app.get("/", response_class=HTMLResponse)
async def homepage(request: Request):
    count = getCount()
    return templates.TemplateResponse("index.html", {"request": request, "count": count[0], "hostname": hostname})

@app.post("/count")
async def add_count():
    updateCount()
    count = getCount()
    return count[0]

def updateCount():
    try:
        global db_user, db_pass, db_host, db_port, db_db
        connection = psycopg2.connect(user=db_user,
                                      password=db_pass,
                                      host=db_host,
                                      port=db_port,
                                      database=db_db)
        cursor = connection.cursor()

        sql_update_query = """Update importantdata set count = count + 1 WHERE id = 1;"""
        cursor.execute(sql_update_query)
        connection.commit()
        count = cursor.rowcount
        logger.info("Record Updated successfully ")

    except (Exception, psycopg2.Error) as error:
        logger.info("Error in update operation", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            logger.info("PostgreSQL connection is closed")

def getCount():
    try:
        global db_user, db_pass, db_host, db_port, db_db    
        connection = psycopg2.connect(user=db_user,
                                      password=db_pass,
                                      host=db_host,
                                      port=db_port,
                                      database=db_db)
        cursor = connection.cursor()

        sql_select_query = """select count from importantdata WHERE id = 1;"""
        cursor.execute(sql_select_query)
        count = cursor.fetchone()
        # logger.info("retrieved count from database: ", str(count[0][0]))

    except (Exception, psycopg2.Error) as error:
        logger.info("Error in update operation", error)

    finally:
        # closing database connection.
        if connection:
            cursor.close()
            connection.close()
            logger.info("PostgreSQL connection is closed")
    
    return count

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)