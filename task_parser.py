from bs4 import BeautifulSoup

def init(argv):
    with open(argv) as task:
        global soup
        soup = BeautifulSoup(task, 'html.parser')

def get_task_id():
    id = soup.body.p.contents[2].strip()
    return id