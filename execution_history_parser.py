from bs4 import BeautifulSoup

def init(html_file):
    with open(html_file) as task:
        global soup
        soup = BeautifulSoup(task, 'html.parser')

def get_start_exe_time(exe):
    return exe[1].find_all('td')[1].text

def get_start_exe_world(exe):
    return exe[1].find_all('td')[2].text

def get_finish_exe_time(exe):
    return exe[2].find_all('td')[1].text

def get_finish_exe_world(exe):
    return exe[2].find_all('td')[2].text

def main(html_file):
    init(html_file)
    exe_list = []
    exe = soup.find(id="execution-history").find_all("div").find_all('tr')
    exe_list.append({'start_execution_time' : get_start_exe_time(exe)})
    exe_list.append({'start_execution_world' : get_start_exe_world(exe)})
    exe_list.append({'finish_execution_time' : get_finish_exe_time(exe)})
    exe_list.append({'finish_execution_world' : get_finish_exe_world(exe)})
    return exe_list