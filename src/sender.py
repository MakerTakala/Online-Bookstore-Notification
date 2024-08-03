import smtplib
from email.mime.text import MIMEText

from base_type import Book


class BookSender:
    """Book sender class"""

    def __init__(self, email_sender: str, email_sender_password: str):
        self.email_sender = email_sender
        self.email_sender_password = email_sender_password

    def create_email_body(self, books: list[Book]):
        """Send books to email"""
        subject = "Today's new books"
        book_show_html = "<h3>Today's new books</h3>"
        for book in books:
            book_show_html += f"""
            <div>
                <h3>{book.title}</h3>
                <a href="{book.link}"><img src="{book.image}" alt="{book.title}" /></a>
                <p>作者: {book.author}</p>
                <p>價格: {book.price}</p>
                <p>出版社: {book.publisher}</p>
                <p>出版日期: {book.publish_date}</p>
                <button><a href="{book.link}">前往購買</a></button>
            </div>
            <br />
            """

        body = f"""
        <html>
            <head></head>
            <body>
                {book_show_html}
            </body>
        </html>
        """
        body = MIMEText(body, "html")
        return subject, body

    def send_email(self, rigisters: list[str], books: list[Book]):
        """Send email"""

        if not books:
            return

        subject, body = self.create_email_body(books)
        msg = body
        msg["Subject"] = subject
        msg["From"] = self.email_sender

        for register in rigisters:
            msg["To"] = register

            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login(self.email_sender, self.email_sender_password)
            server.sendmail(self.email_sender, register, msg.as_string())
            server.quit()
