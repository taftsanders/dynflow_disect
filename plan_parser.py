from bs4 import BeautifulSoup
import yaml
import yaml_poll_attempts
import yaml_pulp_tasks
import uuid
import db_editor as db


create_table_sql = '''CREATE TABLE IF NOT EXISTS plan(
                                task_id text,
                                label text,
                                started_at text,
                                ended_at text,
                                input blob);'''

insert_table_data = '''INSERT INTO plan(
                                    task_id,
                                    label,
                                    started_at,
                                    ended_at,
                                    input)
                                    VALUES (?,?,?,?,?);'''

def init(html_file):
    with open(html_file) as task:
        global soup
        soup = BeautifulSoup(task, 'html.parser')

#Creates a list of dictionaries
# key = plan.label
# value = bs4.element.tag(plan.metadata & plan.input)
def get_plan_actions():
    plan_list = [] 
    iterator = 0 
    dividers = [] 
    for div in soup.find(id="plan").find_all("div"): 
        dividers.append(div) 
    while iterator < len(soup.find(id="plan").find_all('span')): 
        plan_actions = {} 
        label = str(soup.find(id="plan").find_all('span')[iterator].text) 
        plan_actions[label] = dividers[iterator] 
        plan_list.append(plan_actions) 
        iterator += 1 
    return plan_list

def get_label(action):
    for key in action.keys():
        return key

def get_started_at(action):
    for value in action.values():
        return value.find_all('p')[0].contents[1].strip()

def get_ended_at(action):
    for value in action.values():
        return value.find_all('p')[1].contents[1].strip().split('(')[0].strip()

def get_input(action):
    for value in action.values():
        return str(yaml.load(value.find_all('p')[2].pre.text, yaml.Loader))

def gen_uuid():
    return uuid.uuid4()

def main(html_file,task):
    init(html_file)
    task_id = html_file[:-5]
    conn = db.create_connection('/tmp/disect/dynflow_task_'+task_id+'.sqlite.db')
    db.create_table(conn, create_table_sql)
    cur = conn.cursor()
    for action in get_plan_actions():
        plan_actions = ( task,
                                    get_label(action),
                                    get_started_at(action),
                                    get_ended_at(action),
                                    get_input(action))
        cur.execute(insert_table_data, plan_actions)
    conn.commit()

