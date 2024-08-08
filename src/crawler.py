from urllib.parse import quote

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from bs4 import BeautifulSoup

from base_type import Book


class KingstoneCrawler:
    """Crawler for Kingstone"""

    def __init__(self) -> None:
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")

        self.driver = webdriver.Chrome(service=Service(), options=options)
        self.base_url = "https://www.kingstone.com.tw"

    def _url_encode(self, search_query: str) -> str:
        """Encode search query to url"""
        encoded_query = quote(search_query)
        return f"{self.base_url}/search/key/{encoded_query}"

    def _get_html(self, url: str) -> BeautifulSoup:
        """Get html from url"""
        self.driver.get(url)
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def _extract_book_info(self, book_html: BeautifulSoup) -> Book:
        """Get book info from html"""
        title = book_html.find("h3", class_="pdnamebox")
        image = book_html.find("div", class_="coverbox")
        image = image.find("img") if image else None
        tatebetsu = book_html.find("span", class_="book")
        selling_type = book_html.find("div", class_="classbox")
        selling_type = selling_type.find("a") if selling_type else None
        link = book_html.find("div", class_="coverbox")
        link = link.find("a") if link else None
        author = book_html.find("span", class_="author")
        author = author.find("a") if author else None
        discount = book_html.find("b", class_="b1")
        price = book_html.find("div", class_="buymixbox")
        price = price.find("b", class_="") if price else None
        publisher = book_html.find("span", class_="publish")
        publisher = publisher.find("a") if publisher else None
        publish_date = book_html.find("span", class_="pubdate")
        publish_date = publish_date.find("b") if publish_date else None

        title = title.text.strip() if title else ""
        image = image["src"] if image else ""
        tatebetsu = tatebetsu.text.strip() if tatebetsu else ""
        selling_type = selling_type.text.strip() if selling_type else ""
        link = self.base_url + link["href"] if link else ""
        author = author.text.strip() if author else ""
        price = (
            (
                ("" if discount is None else discount.text.strip() + "折 ")
                + f" {price.text.strip()}元"
            )
            if price
            else ""
        )
        publisher = publisher.text.strip() if publisher else ""
        publish_date = (
            publish_date.text.strip().replace("/", "-") if publish_date else ""
        )

        return Book(
            title=title,
            image=image,
            tatebetsu=tatebetsu,
            selling_type=selling_type,
            link=link,
            author=author,
            price=price,
            publisher=publisher,
            publish_date=publish_date,
        )

    def get_books(self, search_query: str) -> list[Book]:
        """Get books from Kingstone"""
        search_url = self._url_encode(search_query)
        page_html = self._get_html(search_url)

        # pages = page_html.find("div", class_="searchResultTitle").text.strip()[-1]
        wait = WebDriverWait(self.driver, 10)
        pages = wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "searchResultTitle"))
        ).text.strip()[-1]

        books_list: list[Book] = []
        for i in range(int(pages)):
            self.driver.get(f"{search_url}/page/{i + 1}")
            page_html = BeautifulSoup(self.driver.page_source, "html.parser")
            books_html = page_html.find_all("li", class_="displayunit")
            for book_html in books_html:
                books_list.append(self._extract_book_info(book_html))
        return books_list
