from typing import List

from fastapi import FastAPI, HTTPException, Depends
from app import book
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor

from . import crud, data, models, schemas
from .data import db_state_default

from mysql.connector import Error
import MySQLdb

from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
#########################################################################################
books: list[book.Book] = [
    book.Book(0, 'Mathematical analysis', 'Text...................................'),
    book.Book(1, 'Mathematical logic', 'Text...................................'),
    book.Book(2, 'Linear algebra', 'Text...................................')
]


def add_book(title: str, body: str):
    _id = len(books)
    books.append(book.Book(_id, title, body))
    return _id

##########################################################################################
# data.mysql_db.connect()
# data.mysql_db.create_tables([models.Book])
# data.mysql_db.close()

app = FastAPI()

# Jaeger#############################################################
resource = Resource(attributes={
    SERVICE_NAME: "books"
})

jaeger_exporter = JaegerExporter(
    agent_host_name="jaeger",
    agent_port=6831,
)

provider = TracerProvider(resource=resource)
processor = BatchSpanProcessor(jaeger_exporter)
provider.add_span_processor(processor)
trace.set_tracer_provider(provider)

FastAPIInstrumentor.instrument_app(app)

# Prometheus#########################################################
from prometheus_fastapi_instrumentator import Instrumentator


@app.on_event("startup")
async def startup():
    Instrumentator().instrument(app).expose(app)

#####################################################################
# async def reset_db_state():
#     data.mysql_db._state._state.set(db_state_default.copy())
#     data.mysql_db._state.reset()


# def get_db(db_state=Depends(reset_db_state)):
#     try:
#         data.mysql_db.connect()
#         yield
#     finally:
#         if not data.mysql_db.is_closed():
#             data.mysql_db.close()

##############################################################################
@app.get("/")
async def check_service():
    return


@app.get("/v1/books")
async def get_books():
    return books


@app.post("/v1/books")
async def add_books(title: str, body: str):
    add_book(title, body)
    return books[-1]


@app.get("/v1/books/{id}")
async def get_books_by_id(id: int):
    info = [item for item in books if item.id == id]
    if len(info) > 0:
        return info[0]
    return HTTPException(status_code=404, detail="Book not found!")

###################################################################################
# @app.post("/books/", response_model=schemas.BookBase)
# def create_book(book: schemas.BookBase):
#     return crud.create_book(book=book)


# @app.post("/books_add/")
# def create_user(title: str, body: str):
#     db = MySQLdb.connect(
#         host='localhost',
#         user='root',
#         passwd='121133',
#         db="micro")
#     cur = db.cursor()
#     cur.execute(f"""INSERT INTO `book` (`title`, `body`) VALUE ('{title}', '{body}');""")
#     db.commit()
#     db.close()
#     return 'Book is added'


# @app.get("/books/", response_model=List[schemas.Book], dependencies=[Depends(get_db)])
# def read_users(skip: int = 0, limit: int = 100):
#     books = crud.get_books(skip=skip, limit=limit)
#     return books
