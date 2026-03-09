from http.server import HTTPServer, SimpleHTTPRequestHandler
import datetime

from jinja2 import Environment, FileSystemLoader, select_autoescape

def ending(num):
    num = num % 100
    if 5 <= num <= 20:
        return 'лет'
    num = num % 10
    if num == 1:
        return 'год'
    elif 2 <= num <= 4:
        return 'года'
    else:
        return 'лет'

env = Environment(
    loader=FileSystemLoader('.'),
    autoescape=select_autoescape(['html', 'xml'])
)

template = env.get_template('template.html')
winery_age_years=datetime.datetime.now().year-1920
age_ending=ending(winery_age_years)
rendered_page = template.render(
    winery_age_years=winery_age_years, 
    age_ending=age_ending,
)

with open('index.html', 'w', encoding="utf8") as file:
    file.write(rendered_page)

server = HTTPServer(('127.0.0.1', 8000), SimpleHTTPRequestHandler)
server.serve_forever()