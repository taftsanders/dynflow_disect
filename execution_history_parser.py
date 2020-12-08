from bs4 import BeautifulSoup
import db_editor as db

create_table_sql = '''CREATE TABLE IF NOT EXISTS exe_history(
                                task_id text,
                                start_time text,
                                start_world text,
                                finish_time text,
                                finish_world text);'''

insert_table_data = '''INSERT INTO exe_history(
                                    task_id,
                                    start_time,
                                    start_world,
                                    finish_time,
                                    finish_world)
                                    VALUES (?,?,?,?,?);'''

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

def main(html_file,task):
    init(html_file)
    task_id = html_file[:-5]
    conn = db.create_connection('/tmp/disect/'+task_id+'.sqlite.db')
    db.create_table(conn, create_table_sql)
    cur = conn.cursor()
    exe = soup.find(id="execution-history").find_all('tr')
    try:
        execution_actions = ( task,
                                            get_start_exe_time(exe),
                                            get_start_exe_world(exe),
                                            get_finish_exe_time(exe),
                                            get_finish_exe_world(exe))
    except  IndexError:
        print('finish executions out of range, task probably isnt finished')
        execution_actions = ( task,
                                            get_start_exe_time(exe),
                                            get_start_exe_world(exe),
                                            'None',
                                            'None')
    cur.execute(insert_table_data, execution_actions)
    conn.commit()
