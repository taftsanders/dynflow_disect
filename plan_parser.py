from bs4 import BeautifulSoup
import db_editor as db
import yaml
import yaml_poll_attempts
import yaml_pulp_tasks


create_table_sql = '''CREATE TABLE IF NOT EXISTS plan(
                                task_id text,
                                label text,
                                started_at text,
                                ended_at text,
                                capsule_id integer,
                                smart_proxy_id integer,
                                smart_proxy_name text,
                                services_checked text,
                                repo_pulp_id text,
                                sync_options text,
                                remote_user text,
                                remote_cp_user text,
                                current_request_id integer,
                                current_timezone text,
                                current_user_id integer,
                                current_organization_id integer,
                                current_location_id integer,
                                input blob);'''

insert_table_data = '''INSERT INTO plan(
                                    task_id,
                                    label,
                                    started_at,
                                    ended_at,
                                    capsule_id,
                                    smart_proxy_id,
                                    smart_proxy_name,
                                    services_checked,
                                    repo_pulp_id,
                                    sync_options,
                                    remote_user,
                                    remote_cp_user,
                                    current_request_id,
                                    current_timezone,
                                    current_user_id,
                                    current_organization_id,
                                    current_location_id,
                                    input)
                                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''

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
        return yaml.load(value.find_all('p')[2].pre.text, yaml.Loader)

def get_input_capsule_id(input_data):
    try:
        return input_data['capsule_id']
    except KeyError:
        return None

def get_input_repo_pulp_id(input_data):
    try:
        return input_data['repo_pulp_id']
    except KeyError:
        return None

def get_input_sync_options(input_data):
    try:
        return str(input_data['sync_options'])
    except KeyError:
        return None

def get_input_remote_user(input_data):
    try:
        return input_data['remote_user']
    except KeyError:
        return None

def get_input_remote_cp_user(input_data):
    try:
        return input_data['remote_cp_user']
    except KeyError:
        return None

def get_input_current_request_id(input_data):
    try:
        return input_data['current_request_id']
    except KeyError:
        return None

def get_input_current_timezone(input_data):
    try:
        return input_data['current_timezone']
    except KeyError:
        return None

def get_input_current_user_id(input_data):
    try:
        return input_data['current_user_id']
    except KeyError:
        return None

def get_input_current_organization_id(input_data):
    try:
        return input_data['current_organization_id']
    except KeyError:
        return None

def get_input_current_location_id(input_data):
    try:
        return input_data['current_location_id']
    except KeyError:
        return None

def get_input_sp_id(input_data):
    try:
        return input_data['smart_proxy']['id']
    except KeyError:
        pass
    try:
        return input_data['smart_proxy_id']
    except KeyError:
        return None

def get_input_sp_name(input_data):
    try:
        return input_data['smart_proxy']['name']
    except KeyError:
        return None

def get_input_svc_checked(input_data):
    try:
        return str(input_data['services_checked'])
    except KeyError:
        return None


def main(html_file,task):
    init(html_file)
    task_id = html_file[:-5]
    conn = db.create_connection('/tmp/disect/'+task_id+'.sqlite.db')
    db.create_table(conn, create_table_sql)
    cur = conn.cursor()
    for action in get_plan_actions():
        input_data = get_input(action)
        plan_actions = ( task,
                                    get_label(action),
                                    get_started_at(action),
                                    get_ended_at(action),
                                    get_input_capsule_id(input_data),
                                    get_input_sp_id(input_data),
                                    get_input_sp_name(input_data),
                                    get_input_svc_checked(input_data),
                                    get_input_repo_pulp_id(input_data),
                                    get_input_sync_options(input_data),
                                    get_input_remote_user(input_data),
                                    get_input_remote_cp_user(input_data),
                                    get_input_current_request_id(input_data),
                                    get_input_current_timezone(input_data),
                                    get_input_current_user_id(input_data),
                                    get_input_current_organization_id(input_data),
                                    get_input_current_location_id(input_data),
                                    str(input_data))
        cur.execute(insert_table_data, plan_actions)
    conn.commit()

