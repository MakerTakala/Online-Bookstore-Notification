class Book:
    """Book class"""

    def __init__(
        self,
        title: str,
        image: str,
        tatebetsu: str,
        selling_type: str,
        link: str,
        author: str,
        price: str,
        publisher: str,
        publish_date: str,
    ):
        self.title = title
        self.image = image
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
        Image: {self.image}
        Tatebetsu: {self.tatebetsu}
        Selling Type: {self.selling_type}
        Link: {self.link}
        Author: {self.author}
        Price: {self.price}
        Publisher: {self.publisher}
        Publish Date: {self.publish_date}
        """
