# Web Scraping with Scrapy

A beginner-friendly web scraping project built using the Scrapy framework in Python.

---

## Quick Links

- [Installation](#installation)
- [Project Structure](#project-structure)
- [Create First Spider](#create-first-spider)


---

## Project Overview

This project is created to learn and practice:

- Basics of the Scrapy framework
- Overview of Spiders and their role in web crawling

---

## Technologies Used

- Python 3
- Scrapy

---

## Installation

### 1. Create Virtual Environment

```bash
python3 -m venv scrapy_env
```

### 2. Activate Virtual Environment

```bash
source scrapy_env/bin/activate
```

### 3. Install Scrapy

```bash
pip install scrapy
```

### 4. Verify Installation

```bash
scrapy version
```

or

```bash
scrapy
```

---

## Create Scrapy Project

```bash
scrapy startproject bookscraper
```

---

## Project Structure

```bash
bookscraper/
│
├── bookscraper/
│   ├── spiders/
│   ├── items.py
│   ├── pipelines.py
│   ├── settings.py
│   └── middlewares.py
│
└── scrapy.cfg
```

---

## Project Structure Explanation

### `scrapy.cfg`
Configuration file used to run Scrapy project commands.

### `bookscraper/`
Main project package containing Scrapy application files.

### `spiders/`
Contains all spider files responsible for crawling websites and extracting data.

### `items.py`
Defines the structure of scraped data using Scrapy Items.

### `pipelines.py`
Used for processing, cleaning, validating, or storing scraped data.

### `settings.py`
Contains project settings such as user agents, delays, pipelines, and middleware configuration.

### `middlewares.py`
Handles request and response processing during crawling.

---

## Create First Spider

### Command

```bash
scrapy genspider quotes quotes.toscrape.com
```

### Explanation

- `genspider` → Creates a new spider
- `quotes` → Spider name
- `quotes.toscrape.com` → Website domain to crawl

This command creates:

```bash
bookscraper/spiders/quotes.py
```

---

### Run Spider Command

```bash
scrapy crawl quotes
```

---

## CSS Selectors

A CSS selector is a pattern used to select and extract elements from an HTML webpage.

It helps Scrapy locate specific data like text, tags, or attributes from the page.

---

### Quick Meaning with Examples

- `tag` → selects HTML tag  
  ```python
  response.css("title")
  ```

- `.class` → selects class name  
  ```python
  response.css(".author")
  ```

- `#id` → selects ID  
  ```python
  response.css("#main")
  ```

- `::text` → extracts text only  
  ```python
  response.css("title::text")
  ```

- `parent child` → selects nested elements  
  ```python
  response.css("div.quote span.text::text")
  ```

## Using Scrapy Shell

Scrapy shell helps inspect and test selectors before writing spiders.

### Open Scrapy Shell

```bash
scrapy shell "https://quotes.toscrape.com/"
```

---

## Extract Page Title

### Get title tag

```python
response.css("title")
```

### Extract title text

```python
response.css("title::text").extract()

```
### Example Output

```python
['Quotes to Scrape']
```

---

### Extract first title text

```python
response.css("title::text").extract_first()
```

### Example Output

```python
'Quotes to Scrape'
```

---

### Extract specific index

```python
response.css("span.text::text")[2].extract()
```

---

## Useful Scrapy Shell Methods

| Method | Description |
|--------|-------------|
| `.extract()` | Returns all matching data as list |
| `.extract_first()` | Returns first matching value safely (returns `None` if empty) |
| `::text` | Extracts only text content |
| `.css()` | Select elements using CSS selectors |
| `[0]` (indexing) | Directly accesses first element, but throws error if empty |

---

# XPath Selector in Scrapy

XPath is a method used to locate and extract data from HTML webpages based on their structure (DOM).

It helps Scrapy find specific elements like text, links, and attributes.

---

## Examples

### Select a tag
```python
response.xpath("//title").extract()
```

---

### Extract text from tag
```python
response.xpath("//title/text()").extract()
```

---

### Select elements by class
```python
response.xpath("//span[@class='text']/text()").extract()
```

---

### Extract all links
```python
response.xpath("//a/@href").extract()
```

---

### Get first element
```python
response.xpath("//span[@class='text']/text()")[0].extract()
```

---
### CSS + XPath (Short)

```python
response.css("li.next a").xpath("@href").extract()
```

➡ Extracts the **next page URL**

- CSS → selects the link element  
- XPath → gets the `href` attribute  

---
## Items in Scrapy

Items are used to define **structured data format** for scraped data.

---

### Define Items (`items.py`)

```python
import scrapy


class QuoteTutorialItem(scrapy.Item):
    title = scrapy.Field()
    author = scrapy.Field()
    tags = scrapy.Field()
```

---

### Using Items in Spider

```python
import scrapy
from ..items import QuoteTutorialItem
```

---

### Why Use Items?

- Keeps data structured
- Makes code cleaner
- Easy to export (JSON, CSV, DB)
- Better project scalability

---
## Key Difference

| Method | Returns | Use Case |
|--------|--------|----------|
| `.extract()` | List | Multiple values (tags, links) |
| `.get()` | Single value | One value (title, author, etc.) |


# Data Export

Scrapy supports exporting scraped data into multiple formats.

---

## Export Commands

### JSON Format
```bash
scrapy crawl quotes -o quotes.json
```
### CSV Format
```bash
scrapy crawl quotes -o quotes.csv
```
### XML Format
```bash
scrapy crawl quotes -o quotes.xml
```