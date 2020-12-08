from bs4 import BeautifulSoup
import db_editor as db

create_table_sql = '''CREATE TABLE IF NOT EXISTS tasks(
                                id text,
                                label text,
                                status text,
                                result text,
                                started_at text,
                                ended_at text);'''

insert_table_data = '''INSERT INTO tasks(
                                    id,
                                    label,
                                    status,
                                    result,
                                    started_at,
                                    ended_at)
                                    VALUES (?,?,?,?,?,?);'''

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
    task_id = html_file[:-5]
    task_metadata = ( get_task_id(),
                                    get_task_label(),
                                    get_task_status(),
                                    get_task_result(),
                                    get_task_started_at(),
                                    get_task_ended_at())
    conn = db.create_connection('/tmp/disect/dynflow_task_'+task_id+'.sqlite.db')
    db.create_table(conn, create_table_sql)
    cur = conn.cursor()
    cur.execute(insert_table_data, task_metadata)
    conn.commit()
    return get_task_id()
