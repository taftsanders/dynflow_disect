from bs4 import BeautifulSoup

def init(html_file):
    with open(html_file) as task:
        global soup
        soup = BeautifulSoup(task, 'html.parser')

def get_plan_actions():
    return soup.find(id="plan").find_all('div')



