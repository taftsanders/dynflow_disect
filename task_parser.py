from bs4 import BeautifulSoup

def init(argv):
    with open(argv) as task:
        global soup
        soup = BeautifulSoup(task, 'html.parser')

def get_task_id():
    id = str(soup.body.contents[1].contents[2]).strip()
    return id

def get_task_label():
    label = str(soup.body.contents[3].contents[2]).strip()
    return label

def get_task_status():
    status = str(soup.body.contents[5].contents[2]).strip()
    return status

def get_task_result():
    result = str(soup.body.contents[7].contents[2]).strip()
    return result

def get_task_started_at():
    started_at = str(soup.body.contents[9].contents[2]).strip()
    return started_at

def get_task_ended_at():
    ended_at = str(soup.body.contents[11].contents[2]).strip()
    return ended_at

def main(html_file):
    init(html_file)
    task = {}
    task['id'] = get_task_id()
    task['label'] = get_task_label()
    task['status'] = get_task_status()
    task['result'] = get_task_result()
    task['started_at'] = get_task_started_at()
    task['ended_at'] = get_task_ended_at()
    return task