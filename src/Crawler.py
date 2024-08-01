# from typing import
from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


class Book:
    """Book class"""

    def __init__(
        self,
        title: str,
        tatebetsu: str,
        selling_type: str,
        link: str,
        author: str,
        price: str,
        publisher: str,
        publish_date: str,
    ):
        self.title = title
        self.tatebetsu = tatebetsu
        self.selling_type = selling_type
        self.link = link
        self.author = author
        self.price = price
        self.publisher = publisher
        self.publish_date = publish_date

    def __str__(self) -> str:
        return f"""
        Title: {self.title}
        Tatebetsu: {self.tatebetsu}
        Selling Type: {self.selling_type}
        Link: {self.link}
        Author: {self.author}
        Price: {self.price}
        Publisher: {self.publisher}
        Publish Date: {self.publish_date}
        """


class KingstoneCrawler:
    """Crawler for Kingstone"""

    def __init__(self) -> None:
        self.driver = webdriver.Chrome()
        self.base_url = "https://www.kingstone.com.tw/"

    def _url_encode(self, search_query: str) -> str:
        """Encode search query to url"""
        encoded_query = quote(search_query)
        return f"{self.base_url}/search/key/{encoded_query}"

    def _get_book_info(self, book_html: BeautifulSoup) -> Book:
        """Get book info from html"""
        title = book_html.find("h3", class_="pdnamebox")
        tatebetsu = book_html.find("span", class_="book")
        selling_type = book_html.find("div", class_="classbox").find("a")
        link = book_html.find("div", class_="coverbox").find("a")
        author = book_html.find("span", class_="author").find("a")
        discount = book_html.find("b", class_="b1")
        price = book_html.find("div", class_="buymixbox").find("b", class_="")
        publisher = book_html.find("span", class_="publish").find("a")
        publish_date = book_html.find("span", class_="pubdate").find("b")

        title = (title.text.strip(),)
        tatebetsu = (tatebetsu.text.strip(),)
        selling_type = (selling_type.text.strip(),)
        link = (self.base_url + link["href"],)
        author = (author.text.strip(),)
        price = (
            ("" if discount is None else discount.text.strip() + "折 ")
            + f" {price.text.strip()}元",
        )
        publisher = (publisher.text.strip(),)
        publish_date = (publish_date.text.strip(),)

        return Book(
            title=title,
            tatebetsu=tatebetsu,
            selling_type=selling_type,
            link=link,
            author=author,
            price=price,
            publisher=publisher,
            publish_date=publish_date,
        )

    def get_books(self, search_query: str):
        """Get books from Kingstone"""
        search_url = self._url_encode(search_query)
        self.driver.get(search_url)
        pages = self.driver.find_element(By.CLASS_NAME, "searchResultTitle").text[-1]
        # book_list: list[Book] = []
        for i in range(int(pages)):
            self.driver.get(f"{search_url}/page/{i}")
            page_html = BeautifulSoup(self.driver.page_source, "html.parser")
            book_list = page_html.find_all("li", class_="displayunit")
            for book_html in book_list:
                self._get_book_info(book_html)
        self.driver.quit()
