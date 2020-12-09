from bs4 import BeautifulSoup
import db_editor as db
import plan_parser as pp
import yaml
import yaml_pulp_tasks
import yaml_poll_attempts


create_table_sql = '''CREATE TABLE IF NOT EXISTS run(
                                task_id text,
                                queue text,
                                label text,
                                started_at text,
                                ended_at text,
                                real_time real,
                                execution_time real,
                                input blob,
                                output blob);'''

insert_table_data = '''INSERT INTO run(
                                    task_id,
                                    queue,
                                    label,
                                    started_at,
                                    ended_at,
                                    real_time,
                                    execution_time,
                                    input,
                                    output)
                                    VALUES (?,?,?,?,?,?,?,?,?);'''

def init(html_file):
    with open(html_file) as task:
        global soup
        soup = BeautifulSoup(task, 'html.parser')

#Creates a list of dictionaries
# key = run.label
# value = bs4.element.tag(run.metadata & run.input & run.output)
def get_run_actions():
    run_list = []
    iterator = 0
    dividers = []
    for div in soup.find(id="run").find_all('div'):
        if 'atom' in str(div):
            continue
        else:
            dividers.append(div)
    while iterator < len(soup.find(id="run").find_all('span')):
        run_actions = {}
        label = str(soup.find(id="run").find_all('span')[iterator].text).strip().split('\n')[0]
        run_actions[label] = dividers[iterator]
        run_list.append(run_actions)
        iterator += 1
    return run_list

def get_queue(action):
    for value in action.values():
        return value.find_all('p')[0].text.split()[1]

def get_label(action):
    for key in action.keys():
        return key

def get_started_at(action):
    for value in action.values():
        return value.find_all('p')[1].contents[1].strip()

def get_ended_at(action):
    for value in action.values():
        return value.find_all('p')[2].contents[1].strip()

def get_real_time(action):
    for value in action.values():
        return value.find_all('p')[3].text.split()[2].split('.')[0]

def get_exe_time(action):
    for value in action.values():
        return value.find_all('p')[4].text.split(':')[1].split('.')[0].strip()

def get_input(action):
    for value in action.values():
        return str(yaml.load(value.find_all('p')[5].pre.text, yaml.Loader))

def get_input_environment_id(input_data):
    try:
        return input_data['environment_id']
    except KeyError:
        return None

def get_input_content_view_id(input_data):
    try:
        return input_data['content_view_id']
    except KeyError:
        return None

def get_input_repository_id(input_data):
    try:
        return input_data['repository_id']
    except KeyError:
        return None

def get_output(action):
    for value in action.values():
        return str(yaml.load(value.find_all('p')[6].pre.text, yaml.Loader))

def main(html_file,task):
    init(html_file)
    task_id = html_file[:-5]
    conn = db.create_connection('/tmp/disect/'+task_id+'.sqlite.db')
    db.create_table(conn, create_table_sql)
    cur = conn.cursor()
    for action in get_run_actions():
        input_data = get_input(action)
        output_data = get_output(action)
        run_actions = ( task,
                                    get_queue(action),
                                    get_label(action),
                                    get_started_at(action),
                                    get_ended_at(action),
                                    get_real_time(action),
                                    get_exe_time(action),
                                    pp.get_input_capsule_id(input_data),
                                    pp.get_input_sp_id(input_data),
                                    get_input_environment_id(input_data),
                                    get_input_content_view_id(input_data),
                                    get_input_repository_id(input_data),
                                    pp.get_input_repo_pulp_id(input_data),
                                    pp.get_input_sync_options(input_data),
                                    pp.get_input_remote_user(input_data),
                                    pp.get_input_remote_cp_user(input_data),
                                    pp.get_input_current_request_id(input_data),
                                    pp.get_input_current_timezone(input_data),
                                    pp.get_input_current_user_id(input_data),
                                    pp.get_input_current_organization_id(input_data),
                                    pp.get_input_current_location_id(input_data),
                                    get_input(action),
                                    get_output(action,))
        cur.execute(insert_table_data, run_actions)
    conn.commit()

