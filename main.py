from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import pandas as pd
import collections
from dotenv import load_dotenv
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape


def get_year_ending(num):
    num = num % 100
    if 5 <= num <= 20:
        return "лет"
    num = num % 10
    if num == 1:
        return "год"
    elif 2 <= num <= 4:
        return "года"
    else:
        return "лет"


def main():
    load_dotenv()
    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )

    file_path = os.getenv("EXCEL_FILE_PATH", "wine3.xlsx")
    default_file = "wine3.xlsx"
    try:
        df = pd.read_excel(file_path, keep_default_na=False)
    except FileNotFoundError:
        df = pd.read_excel(default_file, keep_default_na=False)

    alcohol_product_data = collections.defaultdict(list)

    for category, group_df in df.groupby("Категория"):
        alcohol_product_data[category] = group_df.to_dict("records")

    template = env.get_template("template.html")
    winery_foudation_year = 1920
    winery_age_years = datetime.datetime.now().year - winery_foudation_year
    age_ending = get_year_ending(winery_age_years)
    rendered_page = template.render(
        winery_age_years=winery_age_years,
        age_ending=age_ending,
        alcohol_product_data=list(alcohol_product_data.items()),
    )

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(("127.0.0.1", 8000), SimpleHTTPRequestHandler)
    server.serve_forever()


if __name__ == "__main__":
    main()
