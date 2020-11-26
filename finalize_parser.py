#Here I will parse a finalize HTML task
from bs4 import BeautifulSoup

def init(html_file):
    with open(html_file) as task:
        global soup
        soup = BeautifulSoup(task, 'html.parser')

def main(html_file):
    init(html_file)
    if soup.find(id="finalize").find("table",{"class":"flow squence"}) == None:
        return 'None'
    else:
        return soup.find(id="finalize").find("table",{"class":"flow squence"})