import os
import json

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base, Book, Pagination

load_dotenv()


class BasePipeline:

    model = None
    spider_name = None

    def open_spider(self, spider):

        if spider.name != self.spider_name:
            return

        try:

            print("Connecting to DB...")

            DATABASE_URL = (
                f"postgresql+psycopg2://"
                f"{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
                f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}"
                f"/{os.getenv('DB_NAME')}"
            )

            self.engine = create_engine(DATABASE_URL)

            Base.metadata.create_all(self.engine)

            Session = sessionmaker(bind=self.engine)
            self.session = Session()

            self.session.query(self.model).delete()
            self.session.commit()

            print("Old data cleared")
            print("DB Connected Successfully")

        except Exception as e:
            print("DB CONNECTION ERROR:", e)

    def close_spider(self, spider):

        if spider.name != self.spider_name:
            return

        self.session.close()
        print("DB Session Closed")


class BooksToscrapePipeline(BasePipeline):

    model = Book
    spider_name = "books"

    def process_item(self, item, spider):

        if spider.name != "books":
            return item

        try:

            print(f"Saving: {item.get('title')}")

            book = Book(
                host_url=item.get("host_url"),
                title=item.get("title"),
                price=item.get("price"),
                description=item.get("description"),
                image_url=item.get("image_url"),
                stock=item.get("stock"),
                product_information=json.dumps(
                    item.get("product_information"),
                    ensure_ascii=False
                )
            )

            self.session.add(book)
            self.session.commit()

            print("Saved Successfully")

        except Exception as e:

            self.session.rollback()
            print("INSERT ERROR:", e)

        return item


class PaginationPipeline(BasePipeline):

    model = Pagination
    spider_name = "pagination"

    def process_item(self, item, spider):

        if spider.name != "pagination":
            return item

        try:

            print(f"Saving: {item.get('title')}")

            book = Pagination(
                category=item.get("category"),
                host_url=item.get("host_url"),
                title=item.get("title"),
                price=item.get("price"),
                description=item.get("description"),
                image_url=item.get("image_url"),
                stock=item.get("stock"),
                product_information = item.get("product_information"),
                pagination_url=item.get("pagination_url")
            )

            self.session.add(book)
            self.session.commit()

            print("Saved Successfully")

        except Exception as e:

            self.session.rollback()
            print("INSERT ERROR:", e)

        return item