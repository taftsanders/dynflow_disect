#Here I will parse a finalize HTML task
from bs4 import BeautifulSoup

def init(html_file):
    with open(html_file) as task:
        global soup
        soup = BeautifulSoup(task, 'html.parser')

def main(html_file):
    init(html_file)
    return soup.find(id="finalize").find_all("div")