import os
import argparse
from datetime import datetime

from dotenv import load_dotenv

from base_type import Book
from crawler import KingstoneCrawler
from sender import BookSender


def crawl_books(search_query: list[str]) -> list[Book]:
    """Crawl books from Kingstone"""
    crawler = KingstoneCrawler()
    book_list: list[Book] = []
    for query in search_query:
        book = crawler.get_books(query)
        book_list.extend(book)
    return book_list


def filter_today_books(all_books: list[Book]) -> list[Book]:
    """Filter books"""
    allowed_books: list[Book] = []
    for book in all_books:
        if datetime.today() == book.publish_date:
            allowed_books.append(book)
    return allowed_books


if __name__ == "__main__":
    load_dotenv()
    queries = os.getenv("QUERIES").split(",")
    registers = os.getenv("REGISTER").split(",")
    email_sender = os.getenv("EMAIL_SENDER")
    email_sender_password = os.getenv("EMAIL_SENDER_PASSWORD")
    book_sender = BookSender(email_sender, email_sender_password)

    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true")
    args = parser.parse_args()

    books = crawl_books(queries)
    book_sender.send_email(registers, books if args.test else filter_today_books(books))
