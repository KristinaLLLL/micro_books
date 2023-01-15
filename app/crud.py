from . import models, schemas


def get_books(skip: int = 0, limit: int = 100):
    return list(models.Book.select().offset(skip).limit(limit))


def create_book(book: schemas.Book):
    db_book = models.Book(title=book.title, body=book.body)
    db_book.save()
    return db_book
