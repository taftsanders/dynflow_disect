from bs4 import BeautifulSoup
import db_editor as db

create_table_sql = '''CREATE TABLE IF NOT EXISTS finalize(
                                task_id text,
                                flow_sequence blob);'''

insert_table_data = '''INSERT INTO finalize(
                                    task_id,
                                    flow_sequence)
                                    VALUES (?,?);'''


def init(html_file):
    with open(html_file) as task:
        global soup
        soup = BeautifulSoup(task, 'html.parser')

def main(html_file,task):
    init(html_file)
    task_id = html_file[:-5]
    #conn = db.create_connection('/tmp/disect/'+task_id+'.sqlite.db')
    conn = db.create_connection('/tmp/disect/disect.sqlite.db')
    db.create_table(conn, create_table_sql)
    cur = conn.cursor()
    if soup.find(id="finalize").find("table",{"class":"flow squence"}) == None:
        finalize_actions = (task,
                                        'None')
    else:
        finalize_actions = (task,
                                       soup.find(id="finalize").find("table",{"class":"flow squence"}))
    cur.execute(insert_table_data, finalize_actions)
    conn.commit()
    