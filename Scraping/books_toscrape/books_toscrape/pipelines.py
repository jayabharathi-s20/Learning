import os
import json

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from zoneinfo import ZoneInfo
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

            existing_book=self.session.query(Pagination).filter_by(
                host_url=item.get("host_url")
            ).first()
            if existing_book:
                data_changed=False
                fields_to_check=[
                    "category",
                    "title",
                    "price",
                    "description",
                    "image_url",
                    "stock",
                    "product_information",
                    "pagination_url"
                ]
                for field in fields_to_check:
                    old_value=getattr(existing_book,field)
                    new_value=item.get(field)
                    if old_value!=new_value:
                        setattr(existing_book,field,new_value)
                        data_changed=True


                if data_changed:

                    print(f"Updated: {item.get('title')}")

                else:
                    print(f"No Changes: {item.get('title')}")

            else:

                new_book = Pagination(

                    category=item.get("category"),
                    host_url=item.get("host_url"),

                    title=item.get("title"),
                    price=item.get("price"),
                    description=item.get("description"),

                    image_url=item.get("image_url"),
                    stock=item.get("stock"),

                    product_information=item.get("product_information"),

                    pagination_url=item.get("pagination_url"),


                    
                )

                self.session.add(new_book)

                print(f"Inserted: {item.get('title')}")

            self.session.commit()

        except Exception as e:

            self.session.rollback()

            print("INSERT/UPDATE ERROR:", e)

        return item
            



            