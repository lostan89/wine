from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime
import pandas as pd
import collections

from jinja2 import Environment, FileSystemLoader, select_autoescape


def ending(num):
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

    env = Environment(
        loader=FileSystemLoader("."), autoescape=select_autoescape(["html", "xml"])
    )


    df = pd.read_excel("wine3.xlsx", keep_default_na=False)


    wine_info_list = collections.defaultdict(list)

    for category, group_df in df.groupby("Категория"):
        wine_info_list[category] = group_df.to_dict("records")

    template = env.get_template("template.html")
    winery_age_years = datetime.datetime.now().year - 1920
    age_ending = ending(winery_age_years)
    rendered_page = template.render(
        winery_age_years=winery_age_years,
        age_ending=age_ending,
        wine_info_list=list(wine_info_list.values()),
    )

    with open("index.html", "w", encoding="utf8") as file:
        file.write(rendered_page)

    server = HTTPServer(("127.0.0.1", 8000), SimpleHTTPRequestHandler)
    server.serve_forever()

if __name__ == '__main__':
    main()