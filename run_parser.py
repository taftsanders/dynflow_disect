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
                                input_capsule_id integer,
                                input_smartproxy_id integer,
                                input_environment_id integer,
                                input_content_view_id integer,
                                input_repository_id integer,
                                input_repo_pulp_id text,
                                input_sync_options text,
                                input_current_request_id text,
                                input_current_timezone text,
                                input_current_organization_id integer,
                                input_current_location_id integer,
                                output_pulptask_publish_exception blob,
                                output_pulptask_publish_task_type text,
                                output_pulptask_publish_tags text,
                                output_pulptask_publish_finish_time text,
                                output_pulptask_publish_start_time text,
                                output_pulptask_publish_traceback blob,
                                output_pulptask_publish_progressreport_puppetrepo_module_total_count integer,
                                output_pulptask_publish_progressreport_puppetrepo_module_state text,
                                output_pulptask_publish_progressreport_puppetrepo_publish_http text,
                                output_pulptask_publish_progressreport_puppetrepo_publish_https text,
                                output_pulptask_publish_progressreport_puppetrepo_meta_state text,
                                output_pulptask_publish_progressreport_puppetrepo_meta_error_message blob,
                                output_pulptask_publish_queue text,
                                output_pulptask_publish_state text,
                                output_pulptask_publish_worker_name text,
                                output_pulptask_publish_result_result text,
                                output_pulptask_publish_result_repo_id text,
                                output_pulptask_publish_result_started text,
                                output_pulptask_publish_result_completed text,
                                output_pulptask_publish_result_distributor_type_id text,
                                output_pulptask_publish_result_distributor_id text,
                                output_pulptask_publish_id text,
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
                                input_capsule_id,
                                input_smartproxy_id,
                                input_environment_id,
                                input_content_view_id,
                                input_repository_id,
                                input_repo_pulp_id,
                                input_sync_options,
                                input_current_request_id,
                                input_current_timezone,
                                input_current_organization_id,
                                input_current_location_id,
                                output_pulptask_publish_exception,
                                output_pulptask_publish_task_type,
                                output_pulptask_publish_tags,
                                output_pulptask_publish_finish_time,
                                output_pulptask_publish_start_time,
                                output_pulptask_publish_traceback,
                                output_pulptask_publish_progressreport_puppetrepo_module_total_count,
                                output_pulptask_publish_progressreport_puppetrepo_module_state,
                                output_pulptask_publish_progressreport_puppetrepo_publish_http,
                                output_pulptask_publish_progressreport_puppetrepo_publish_https,
                                output_pulptask_publish_progressreport_puppetrepo_meta_state,
                                output_pulptask_publish_progressreport_puppetrepo_meta_error_message,
                                output_pulptask_publish_queue,
                                output_pulptask_publish_state,
                                output_pulptask_publish_worker_name,
                                output_pulptask_publish_result_result,
                                output_pulptask_publish_result_repo_id,
                                output_pulptask_publish_result_started,
                                output_pulptask_publish_result_completed,
                                output_pulptask_publish_result_distributor_type_id,
                                output_pulptask_publish_result_distributor_id,
                                output_pulptask_publish_id,
                                input,
                                output)
                                    VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''

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
    if output_data['pulp_tasks']:
        try:
            sync = get_pulp_tasks(output_data)
            return sync[1]
        except KeyError:
            return None
    else: 
        return None

'''Example:
{'exception': None,
 'task_type': 'pulp.server.managers.repo.sync.sync',
 '_href': '/pulp/api/v2/tasks/194abc9e-7f15-45ee-b26c-48db237fd107/',
 'task_id': '194abc9e-7f15-45ee-b26c-48db237fd107',
 'tags': ['pulp:repository:9fe1900e-5bd0-42e5-8791-f769d3b7f226',
  'pulp:action:sync'],
 'finish_time': '2020-11-17T20:34:18Z',
 '_ns': 'task_status',
 'start_time': '2020-11-17T20:34:14Z',
 'traceback': None,
 'spawned_tasks': [{'_href': '/pulp/api/v2/tasks/e7f1186d-43fb-4b6c-a7e1-e74b7b91ce17/',
   'task_id': 'e7f1186d-43fb-4b6c-a7e1-e74b7b91ce17'}],
 'progress_report': {'puppet_importer': {'modules': {'error_message': None,
    'execution_time': 2,
    'total_count': 1,
    'traceback': None,
    'individual_errors': [],
    'state': 'success',
    'error_count': 0,
    'error': 'None',
    'finished_count': 1},
   'metadata': {'query_finished_count': 1,
    'traceback': None,
    'execution_time': 1,
    'query_total_count': 1,
    'error_message': None,
    'state': 'success',
    'error': 'None',
    'current_query': 'http://satellite.zircon.local/pulp/puppet/9fe1900e-5bd0-42e5-8791-f769d3b7f226/modules.json'}}},
 'queue': 'reserved_resource_worker-1@capsule1.zircon.local.dq2',
 'state': 'finished',
 'worker_name': 'reserved_resource_worker-1@capsule1.zircon.local',
 'result': {'result': 'success',
  'importer_id': 'puppet_importer',
  'exception': None,
  'repo_id': '9fe1900e-5bd0-42e5-8791-f769d3b7f226',
  'traceback': None,
  'started': '2020-11-17T20:34:14Z',
  '_ns': 'repo_sync_results',
  'completed': '2020-11-17T20:34:17Z',
  'importer_type_id': 'puppet_importer',
  'error_message': None,
  'summary': {'total_execution_time': 3},
  'added_count': 1,
  'removed_count': 0,
  'updated_count': 0,
  'id': '5fb433c96884fd1913d484e5',
  'details': {'finished_count': 1, 'total_count': 1, 'error_count': 0}},
 'error': None,
 '_id': {'$oid': '5fb433c5d7bb7db61b375d27'},
 'id': '5fb433c5d7bb7db61b375d27'}
 '''
 
def get_pt_sync_exception(output_data):
    try:
        return get_pulp_task_sync(output_data)['exception']
    except (KeyError, TypeError):
        return None

def get_pt_sync_task_type(output_data):
    try:
        return get_pulp_task_sync(output_data)['task_type']
    except (KeyError, TypeError):
        return None

def get_pt_sync_href(output_data):
    try:
        return get_pulp_task_sync(output_data)['_href']
    except (KeyError, TypeError):
        return None

def get_pt_sync_task_id(output_data):
    try:
        return get_pulp_task_sync(output_data)['task_id']
    except (KeyError, TypeError):
        return None

def get_pt_sync_tags(output_data):
    try:
        return get_pulp_task_sync(output_data)['tags']
    except (KeyError, TypeError):
        return None

def get_pt_sync_finish_time(output_data):
    try:
        return get_pulp_task_sync(output_data)['finish_time']
    except (KeyError, TypeError):
        return None

def get_pt_sync_ns(output_data):
    try:
        return get_pulp_task_sync(output_data)['_ns']
    except (KeyError, TypeError):
        return None

def get_pt_sync_start_time(output_data):
    try:
        return get_pulp_task_sync(output_data)['start_time']
    except (KeyError, TypeError):
        return None

def get_pt_sync_traceback(output_data):
    try:
        return get_pulp_task_sync(output_data)['traceback']
    except (KeyError, TypeError):
        return None

def get_pt_sync_spawned_tasks(output_data):
    try:
        return get_pulp_task_sync(output_data)['spawned_tasks']
    except (KeyError, TypeError):
        return None

def get_pt_sync_progress_report(output_data):
    try:
        return get_pulp_task_sync(output_data)['progress_report']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_puppet_importer(output_data):
    try:
        return get_pt_sync_progress_report(output_data)['puppet_importer']
    except (KeyError, TypeError):
        return None

# 'progress_report': {'puppet_importer': {'modules': {
def get_pt_sync_pr_pup_imp_modules(output_data):
    try:
        return get_pt_sync_pr_puppet_importer(output_data)['modules']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_mod_error_message(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['error_message']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_mod_execution_time(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['execution_time']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_mod_total_count(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['total_coun']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_mod_traceback(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['traceback']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_mod_individual_errors(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['individual_errors']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_mod_state(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['state']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_mod_error_count(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['error_count']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_mod_error(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['error']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_mod_finished_count(output_data):
    try:
        return get_pt_sync_pr_pup_imp_modules(output_data)['finished_count']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_metadata(output_data):
    try:
        return get_pt_sync_pr_puppet_importer(output_data)['metadata']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_meta_query_fin_count(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['query_finished_count']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_meta_traceback(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['traceback']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_meta_execution_time(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['execution_time']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_meta_query_total_count(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['query_total_count']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_meta_error_message(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['error_message']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_meta_state(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['state']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_meta_error(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['error']
    except (KeyError, TypeError):
        return None

def get_pt_sync_pr_pup_imp_meta_current_query(output_data):
    try:
        return get_pt_sync_pr_pup_imp_metadata(output_data)['current_query']
    except (KeyError, TypeError):
        return None

def get_pt_sync_queue(output_data):
    try:
        return get_pulp_task_sync(output_data)['queue']
    except (KeyError, TypeError):
        return None

def get_pt_sync_state(output_data):
    try:
        return get_pulp_task_sync(output_data)['state']
    except (KeyError, TypeError):
        return None

def get_pt_sync_worker_name(output_data):
    try:
        return get_pulp_task_sync(output_data)['worker_name']
    except (KeyError, TypeError):
        return None

def get_pt_sync_result(output_data):
    try:
        return get_pulp_task_sync(output_data)['result']
    except (KeyError, TypeError):
        return None

def get_pt_sync_result_result(output_data):
    try:
        return get_pt_sync_result(output_data)['result']
    except (KeyError, TypeError):
        return None

def get_pt_sync_result_importer_id(output_data):
    try:
        return get_pt_sync_result(output_data)['importer_id']
    except (KeyError, TypeError):
        return None
        
def get_pt_sync_result_exception(output_data):
    try:
        return get_pt_sync_result(output_data)['exception']
    except (KeyError, TypeError):
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

def get_pt_pub_exception(output_data):
    try:
        return get_pulp_task_publish(output_data)['exception']
    except (KeyError, TypeError):
        return None

def get_pt_pub_task_type(output_data):
    try:
        return get_pulp_task_publish(output_data)['task_type']
    except (KeyError, TypeError):
        return None

def get_pt_pub_href(output_data):
    try:
        return get_pulp_task_publish(output_data)['_href']
    except KeyError:
        return None

def get_pt_pub_task_id(output_data):
    try:
        return get_pulp_task_publish(output_data)['task_id']
    except KeyError:
        return None

def get_pt_pub_tags(output_data):
    try:
        return get_pulp_task_publish(output_data)['tags']
    except (KeyError, TypeError):
        return None

def get_pt_pub_finish_time(output_data):
    try:
        return get_pulp_task_publish(output_data)['finish_time']
    except (KeyError, TypeError):
        return None

def get_pt_pub_ns(output_data):
    try:
        return get_pulp_task_publish(output_data)['_ns']
    except KeyError:
        return None

def get_pt_pub_start_time(output_data):
    try:
        return get_pulp_task_publish(output_data)['start_time']
    except (KeyError, TypeError):
        return None

def get_pt_pub_traceback(output_data):
    try:
        return get_pulp_task_publish(output_data)['traceback']
    except (KeyError, TypeError):
        return None

def get_pt_pub_spawned_tasks(output_data):
    try:
        return get_pulp_task_publish(output_data)['spawned_tasks']
    except KeyError:
        return None

def get_pt_pub_progress_report(output_data):
    try:
        return get_pulp_task_publish(output_data)['progress_report']
    except (KeyError, TypeError):
        return None

def get_pt_pub_pr_key(output_data):
    try: 
        for key in get_pt_pub_progress_report(output_data).keys():
            return key
    except (KeyError, TypeError, AttributeError):
        return None

def get_pt_pub_pr_puprepo_modules(output_data):
    try:
        return get_pulp_task_publish(output_data)[get_pt_pub_pr_key(output_data)]['modules']
    except (KeyError, TypeError):
        return None

def get_pt_pub_pr_puprepo_mod_error_messages(output_data):
    try:
        return get_pt_pub_pr_puprepo_modules(output_data)['error_messsage']
    except KeyError:
        return None

def get_pt_pub_pr_puprepo_mod_execution_time(output_data):
    try:
        return get_pt_pub_pr_puprepo_modules(output_data)['execution_time']
    except KeyError:
        return None

def get_pt_pub_pr_puprepo_mod_total_count(output_data):
    try:
        return get_pt_pub_pr_puprepo_modules(output_data)['total_count']
    except (KeyError, TypeError):
        return None

def get_pt_pub_pr_puprepo_mod_traceback(output_data):
    try:
        return get_pt_pub_pr_puprepo_modules(output_data)['traceback']
    except KeyError:
        return None

def get_pt_pub_pr_puprepo_mod_individual_errors(output_data):
    try:
        return get_pt_pub_pr_puprepo_modules(output_data)['individual_errors']
    except KeyError:
        return None

def get_pt_pub_pr_puprepo_mod_state(output_data):
    try:
        return get_pt_pub_pr_puprepo_modules(output_data)['state']
    except (KeyError, TypeError):
        return None

def get_pt_pub_pr_puprepo_mod_error_count(output_data):
    try:
        return get_pt_pub_pr_puprepo_modules(output_data)['error_count']
    except KeyError:
        return None

def get_pt_pub_pr_puprepo_mod_error(output_data):
    try:
        return get_pt_pub_pr_puprepo_modules(output_data)['error']
    except KeyError:
        return None

def get_pt_pub_pr_puprepo_mod_finished_count(output_data):
    try:
        return get_pt_pub_pr_puprepo_modules(output_data)['finished_count']
    except KeyError:
        return None

def get_pt_pub_pr_puprepo_publishing(output_data):
    try:
        return get_pulp_task_publish(output_data)[get_pt_pub_pr_key(output_data)]['publishing']
    except (KeyError, TypeError):
        return None

def get_pt_pub_pr_puprepo_pub_http(output_data):
    try:
        return get_pt_pub_pr_puprepo_publishing(output_data)['http']
    except (KeyError, TypeError):
        return None

def get_pt_pub_pr_puprepo_pub_https(output_data):
    try:
        return get_pt_pub_pr_puprepo_publishing(output_data)['https']
    except (KeyError, TypeError):
        return None

def get_pt_pub_pr_puprepo_metadata(output_data):
    try:
        return get_pulp_task_publish(output_data)[get_pt_pub_pr_key(output_data)]['metadata']
    except (KeyError, TypeError):
        return None

def get_pt_pub_pr_puprepo_meta_execution_time(output_data):
    try:
        return get_pt_pub_pr_puprepo_metadata(output_data)['exceution_time']
    except KeyError:
        return None

def get_pt_pub_pr_puprepo_meta_state(output_data):
    try:
        return get_pt_pub_pr_puprepo_metadata(output_data)['state']
    except (KeyError, TypeError):
        return None

def get_pt_pub_pr_puprepo_meta_error_message(output_data):
    try:
        return get_pt_pub_pr_puprepo_metadata(output_data)['error_message']
    except (KeyError, TypeError):
        return None

def get_pt_pub_pr_puprepo_meta_error(output_data):
    try:
        return get_pt_pub_pr_puprepo_metadata(output_data)['error']
    except KeyError:
        return None

def get_pt_pub_pr_puprepo_meta_traceback(output_data):
    try:
        return get_pt_pub_pr_puprepo_metadata(output_data)['traceback']
    except KeyError:
        return None

def get_pt_pub_queue(output_data):
    try:
        return get_pulp_task_publish(output_data)['queue']
    except (KeyError, TypeError):
        return None

def get_pt_pub_state(output_data):
    try:
        return get_pulp_task_publish(output_data)['state']
    except (KeyError, TypeError):
        return None

def get_pt_pub_worker_name(output_data):
    try:
        return get_pulp_task_publish(output_data)['worker_name']
    except (KeyError, TypeError):
        return None

def get_pt_pub_result(output_data):
    try:
        return get_pulp_task_publish(output_data)['result']
    except (KeyError, TypeError):
        return None

def get_pt_pub_res_result(output_data):
    try:
        return get_pt_pub_result(output_data)['result']
    except (KeyError, TypeError):
        return None

def get_pt_pub_res_exception(output_data):
    try:
        return get_pt_pub_result(output_data)['exception']
    except KeyError:
        return None

def get_pt_pub_res_repo_id(output_data):
    try:
        return get_pt_pub_result(output_data)['repo_id']
    except (KeyError, TypeError):
        return None

def get_pt_pub_res_started(output_data):
    try:
        return get_pt_pub_result(output_data)['started']
    except (KeyError, TypeError):
        return None

def get_pt_pub_res_ns(output_data):
    try:
        return get_pt_pub_result(output_data)['_ns']
    except (KeyError, TypeError):
        return None

def get_pt_pub_res_completed(output_data):
    try:
        return get_pt_pub_result(output_data)['completed']
    except (KeyError, TypeError):
        return None

def get_pt_pub_res_traceback(output_data):
    try:
        return get_pt_pub_result(output_data)['traceback']
    except (KeyError, TypeError):
        return None

def get_pt_pub_res_distributor_type_id(output_data):
    try:
        return get_pt_pub_result(output_data)['distributor_type_id']
    except (KeyError, TypeError):
        return None

def get_pt_pub_res_summary(output_data):
    try:
        return get_pt_pub_result(output_data)['summary']
    except KeyError:
        return None

def get_pt_pub_res_error_message(output_data):
    try:
        return get_pt_pub_result(output_data)['error_message']
    except KeyError:
        return None

def get_pt_pub_res_distributor_id(output_data):
    try:
        return get_pt_pub_result(output_data)['distributor_id']
    except (KeyError, TypeError):
        return None

def get_pt_pub_res_id(output_data):
    try:
        return get_pt_pub_result(output_data)['id']
    except KeyError:
        return None

def get_pt_pub_res_details(output_data):
    try:
        return get_pt_pub_result(output_data)['details']
    except KeyError:
        return None

def get_pt_pub_error(output_data):
    try:
        return get_pulp_task_publish(output_data)['error']
    except KeyError:
        return None

def get_pt_pub_oid(output_data):
    try:
        return get_pulp_task_publish(output_data)['_id']['$oid']
    except KeyError:
        return None

def get_pt_pub_id(output_data):
    try:
        return get_pulp_task_publish(output_data)['id']
    except (KeyError, TypeError):
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
                                    pp.get_input_current_request_id(input_data),
                                    pp.get_input_current_timezone(input_data),
                                    pp.get_input_current_organization_id(input_data),
                                    pp.get_input_current_location_id(input_data),
                                    get_pt_pub_exception(output_data),
                                    get_pt_pub_task_type(output_data),
                                    str(get_pt_pub_tags(output_data)),
                                    get_pt_pub_finish_time(output_data),
                                    get_pt_pub_start_time(output_data),
                                    get_pt_pub_traceback(output_data),
                                    get_pt_pub_pr_puprepo_mod_total_count(output_data),
                                    get_pt_pub_pr_puprepo_mod_state(output_data),
                                    get_pt_pub_pr_puprepo_pub_http(output_data),
                                    get_pt_pub_pr_puprepo_pub_https(output_data),
                                    get_pt_pub_pr_puprepo_meta_state(output_data),
                                    get_pt_pub_pr_puprepo_meta_error_message(output_data),
                                    get_pt_pub_queue(output_data),
                                    get_pt_pub_state(output_data),
                                    get_pt_pub_worker_name(output_data),
                                    get_pt_pub_res_result(output_data),
                                    get_pt_pub_res_repo_id(output_data),
                                    get_pt_pub_res_started(output_data),
                                    get_pt_pub_res_completed(output_data),
                                    get_pt_pub_res_distributor_type_id(output_data),
                                    get_pt_pub_res_distributor_id(output_data),
                                    get_pt_pub_id(output_data),
                                    str(get_input(action)),
                                    str(get_output(action)))
        cur.execute(insert_table_data, run_actions)
    conn.commit()

