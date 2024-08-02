import os
import smtplib
from datetime import datetime
from email.mime.text import MIMEText


from base_type import Book
from crawler import KingstoneCrawler


def crawl_books(search_query: list[str]) -> list[Book]:
    """Crawl books from Kingstone"""
    crawler = KingstoneCrawler()
    book_list: list[Book] = []
    for query in search_query:
        book = crawler.get_books(query)
        book_list.extend(book)
    return book_list


def filter_books(books: list[Book]) -> list[Book]:
    """Filter books"""
    allowed_books: list[Book] = []
    for book in books:
        if datetime.today() == book.publish_date:
            allowed_books.append(book)
    return allowed_books


def send_email(subject, body, to_email):
    """Send email"""
    from_email = os.getenv("EMAIL_USER")
    from_password = os.getenv("EMAIL_PASSWORD")

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
    server.login(from_email, from_password)
    server.sendmail(from_email, to_email, msg.as_string())
    server.quit()


def send_books(books: list[Book]):
    """Send books to email"""
    subject = "Today's new books"
    context = "Today's new books are:\n"
    book_show_html = ""
    for book in books:
        book_show_html += f"""
        <div>
            <h3>{book.title}</h3>
            <img src="{book.image}" alt="{book.title}" />
            <p>作者: {book.author}</p>
            <p>價格: {book.price}</p>
            <p>出版社: {book.publisher}</p>
            <p>出版日期: {book.publish_date}</p>
            <a href="{book.link}">連結</a>
        </div>
        """
    part1 = MIMEText(context, "plain")
    part2 = MIMEText(book_show_html, "html")
    body = f"{part1.as_string()}\n{ part2.as_string()}"
    send_email(subject, body, os.getenv("EMAIL_USER"))


if __name__ == "__main__":
    trace_books_name = os.getenv("QUERIES").split(",")
    result_books = filter_books(crawl_books(trace_books_name))
    if result_books:
        send_books(result_books)
