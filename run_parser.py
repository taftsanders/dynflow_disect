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
        return yaml.load(value.find_all('p')[5].pre.text, yaml.Loader)

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
        return yaml.load(value.find_all('p')[6].pre.text, yaml.Loader)

def get_pulp_tasks(output_data):
    try:
        return output_data['pulp_tasks']
    except KeyError:
        return None

def get_pulp_task_sync(output_data):
    try:
        sync = get_pulp_tasks(output_data)
        return sync[0]
    except KeyError:
        return None

def get_pulp_task_publish(output_data):
    try:
        sync = get_pulp_tasks(output_data)
        return sync[1]
    except KeyError:
        return None

def get_pt_sync_exception(output_data):
    try:
        return get_pulp_task_sync(output_data)['exception']
    except KeyError:
        return None

def get_pt_sync_task_type(output_data):
    try:
        return get_pulp_task_sync(output_data)['task_type']
    except KeyError:
        return None

def get_pt_sync_href(output_data):
    try:
        return get_pulp_task_sync(output_data)['_href']
    except KeyError:
        return None

def get_pt_sync_task_id(output_data):
    try:
        return get_pulp_task_sync(output_data)['task_id']
    except KeyError:
        return None

def get_pt_sync_tags(output_data):
    try:
        return get_pulp_task_sync(output_data)['tags']
    except KeyError:
        return None

def get_pt_sync_finish_time(output_data):
    try:
        return get_pulp_task_sync(output_data)['finish_time']
    except KeyError:
        return None

def get_pt_sync_ns(output_data):
    try:
        return get_pulp_task_sync(output_data)['_ns']
    except KeyError:
        return None

def get_pt_sync_start_time(output_data):
    try:
        return get_pulp_task_sync(output_data)['start_time']
    except KeyError:
        return None

def get_pt_sync_traceback(output_data):
    try:
        return get_pulp_task_sync(output_data)['traceback']
    except KeyError:
        return None

def get_pt_sync_spawned_tasks(output_data):
    try:
        return get_pulp_task_sync(output_data)['spawned_tasks']
    except KeyError:
        return None

def get_pt_sync_progress_report(output_data):
    try:
        return get_pulp_task_sync(output_data)['progress_report']
    except KeyError:
        return None

def get_pt_sync_pr_puppet_importer(output_data):
    try:
        return get_pt_sync_progress_report(output_data)['puppet_importer']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_modules(output_data):
    try:
        return get_pt_sync_pr_puppet_importer(output_data)['modules']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_mod_error_message(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['error_message']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_mod_execution_time(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['execution_time']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_mod_total_count(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['total_coun']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_mod_traceback(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['traceback']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_mod_individual_errors(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['individual_errors']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_mod_state(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['state']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_mod_error_count(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['error_count']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_mod_error(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['error']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_mod_finished_count(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['finished_count']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_metadata(output_data):
    try:
        return get_pt_sync_pr_puppet_importer(output_data)['metadata']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_meta_query_fin_count(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['query_finished_count']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_meta_traceback(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['traceback']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_meta_execution_time(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['execution_time']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_meta_query_total_count(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['query_total_count']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_meta_error_message(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['error_message']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_meta_state(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['state']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_meta_error(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['error']
    except KeyError:
        return None

def get_pt_sync_pr_pup_imp_meta_current_query(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['current_query']
    except KeyError:
        return None

def get_pt_sync_queue(output_data):
    try:
        return get_pulp_task_sync(output_data)['queue']
    except KeyError:
        return None

def get_pt_sync_state(output_data):
    try:
        return get_pulp_task_sync(output_data)['state']
    except KeyError:
        return None

def get_pt_sync_worker_name(output_data):
    try:
        return get_pulp_task_sync(output_data)['worker_name']
    except KeyError:
        return None

def get_pt_sync_result(output_data):
    try:
        return get_pulp_task_sync(output_data)['result']
    except KeyError:
        return None

def get_pt_sync_result_result(output_data):
    try:
        return get_pt_sync_result(output_data)['result']
    except KeyError:
        return None

def get_pt_sync_result_importer_id(output_data):
    try:
        return get_pt_sync_result(output_data)['importer_id']
    except KeyError:
        return None
        
def get_pt_sync_result_exception(output_data):
    try:
        return get_pt_sync_result(output_data)['exception']
    except KeyError:
        return None
        
def get_pt_sync_result_repo_id(output_data):
    try:
        return get_pt_sync_result(output_data)['repo_id']
    except KeyError:
        return None
        
def get_pt_sync_result_traceback(output_data):
    try:
        return get_pt_sync_result(output_data)['traceback']
    except KeyError:
        return None
        
def get_pt_sync_result_started(output_data):
    try:
        return get_pt_sync_result(output_data)['started']
    except KeyError:
        return None
        
def get_pt_sync_result_ns(output_data):
    try:
        return get_pt_sync_result(output_data)['_ns']
    except KeyError:
        return None
        
def get_pt_sync_result_completed(output_data):
    try:
        return get_pt_sync_result(output_data)['completed']
    except KeyError:
        return None
        
def get_pt_sync_result_importer_type_id(output_data):
    try:
        return get_pt_sync_result(output_data)['importer_type_id']
    except KeyError:
        return None
        
def get_pt_sync_result_error_message(output_data):
    try:
        return get_pt_sync_result(output_data)['error_message']
    except KeyError:
        return None
        
def get_pt_sync_result_summary(output_data):
    try:
        return get_pt_sync_result(output_data)['summary']
    except KeyError:
        return None

def get_pt_sync_result_sum_total_exe_time(output_data):
    try:
        return get_pt_sync_result_summary(output_data)['total_execution_time']
    except KeyError:
        return None
        
def get_pt_sync_result_added_count(output_data):
    try:
        return get_pt_sync_result(output_data)['added_count']
    except KeyError:
        return None
        
def get_pt_sync_result_removed_count(output_data):
    try:
        return get_pt_sync_result(output_data)['removed_count']
    except KeyError:
        return None
        
def get_pt_sync_result_updated_count(output_data):
    try:
        return get_pt_sync_result(output_data)['updated_count']
    except KeyError:
        return None
        
def get_pt_sync_result_id(output_data):
    try:
        return get_pt_sync_result(output_data)['id']
    except KeyError:
        return None
        
def get_pt_sync_result_details(output_data):
    try:
        return get_pt_sync_result(output_data)['details']
    except KeyError:
        return None
    
def get_pt_sync_error(output_data):
    try:
        return get_pulp_task_sync(output_data)['error']
    except KeyError:
        return None

def get_pt_sync_id(output_data):
    try:
        return get_pulp_task_sync(output_data)['id']
    except KeyError:
        return None

'''
Publish:
{'exception': None,
 'task_type': 'pulp.server.managers.repo.publish.publish',
 '_href': '/pulp/api/v2/tasks/e7f1186d-43fb-4b6c-a7e1-e74b7b91ce17/',
 'task_id': 'e7f1186d-43fb-4b6c-a7e1-e74b7b91ce17',
 'tags': ['pulp:repository:9fe1900e-5bd0-42e5-8791-f769d3b7f226',
  'pulp:action:publish'],
 'finish_time': '2020-11-17T22:51:19Z',
 '_ns': 'task_status',
 'start_time': '2020-11-17T22:51:18Z',
 'traceback': None,
 'spawned_tasks': [],
 'progress_report': 
    {'9fe1900e-5bd0-42e5-8791-f769d3b7f226_puppet': 
        {'modules': 
            {'error_message': None,
            'execution_time': 0,
            'total_count': 1,
            'traceback': None,
            'individual_errors': None,
            'state': 'success',
            'error_count': 0,
            'error': 'None',
            'finished_count': 1},
        'publishing': {'http': 'success', 'https': 'success'},
        'metadata': {'execution_time': 0,
            'state': 'success',
            'error_message': None,
            'error': 'None',
            'traceback': None}}},
 'queue': 'reserved_resource_worker-2@capsule1.zircon.local.dq2',
 'state': 'finished',
 'worker_name': 'reserved_resource_worker-2@capsule1.zircon.local',
 'result': 
    {'result': 'success',
    'exception': None,
    'repo_id': '9fe1900e-5bd0-42e5-8791-f769d3b7f226',
    'started': '2020-11-17T22:51:18Z',
    '_ns': 'repo_publish_results',
    'completed': '2020-11-17T22:51:18Z',
    'traceback': None,
    'distributor_type_id': 'puppet_distributor',
    'summary': {'total_execution_time': 0},
    'error_message': None,
    'distributor_id': '9fe1900e-5bd0-42e5-8791-f769d3b7f226_puppet',
    'id': '5fb453e66884fd193024f9f0',
    'details': {}},
 'error': None,
 '_id': {'$oid': '5fb433cad7bb7db61b376174'},
 'id': '5fb433cad7bb7db61b376174'}

'''

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
                                    str(get_input(action)),
                                    str(get_output(action)))
        cur.execute(insert_table_data, run_actions)
    conn.commit()

