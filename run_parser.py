#Here I will parse the html for a run method
from bs4 import BeautifulSoup
import yaml

# The entire task page
def init(html_file):
    with open(html_file) as task:
        global soup
        soup = BeautifulSoup(task, 'html.parser')

# All sub actions on the RUN tab
def get_subtasks(html_file):
    global sub_tasks
    sub_tasks = []
    for element in soup.body.find_all('table')[0].contents:
        if element == '\n':
            continue
        else:
            sub_tasks.append(element)

# All blue sectioned boxes
def get_sequence(sub_tasks):
    sequence = []
    for element in sub_tasks:
        if element == '\n':
            continue
        else:
            sequence.append(element.find_all('table'))
    return sequence

#All orange boxes
def get_method(sequence):
    method = []
    for element in sequence:
        method.append(element.find('table'))
    return method

# The label on each orange box
def get_label(method):
    label = str(method.span.string).split()[1]
    return label



# Dynflow details for each method
def get_method_queue(method):
    queue = str(method.find_all('p')[0].contents[1]).strip()
    return queue

def get_started_at(method):
    started_at = str(method.find_all('p')[1].contents[1]).strip()
    return started_at

def get_ended_at(method):
    ended_at = str(method.find_all('p')[2].contents[1]).strip()
    return ended_at

def get_real_time(method):
    real_time = str(method.find_all('p')[3].contents[1]).strip()
    return real_time

def get_exe_time(method):
    exe_time = str(method.find_all('p')[4].contents[1]).strip()
    return exe_time
#END OF DYNFLOW DETAILS COLLECTION


# Get INPUT section of method
def get_input(method):
    global method_input
    method_input = yaml.load(method.find_all('p')[5].find('pre').string)

def get_capsule_id(method_input):
    capsule_id = method_input.get('capsule_id')
    return capsule_id

def get_repo_id(method_input):
    repo_id = method_input.get('repo_id')
    return repo_id

def get_repo_pulp_id(method_input):
    repo_pulp_id = method_input.get('repo_pulp_id')
    return repo_pulp_id

def get_sync_options(method_input):
    sync_options = method_input.get('sync_options')
    return sync_options

def get_remote_user(method_input):
    remote_user = method_input.get('remote_user')
    return remote_user

def get_remote_cp_user(method_input):
    remote_cp_user = method_input.get('remote_cp_user')
    return remote_cp_user

def get_current_tz(method_input):
    current_tz = method_input.get('current_timezone')
    return current_tz

def get_current_user_id(method_input):
    current_user = method_input.get('current_user')
    return current_user

def get_current_org_id(method_input):
    current_org_id = method_input.get('current_organization_id')
    return current_org_id

def get_current_location_id(method_input):
    current_location_id = method_input.get('current_location_id')
    return current_location_id
#END OF INPUT COLLECTION


# Get OUTPUT section of method 
def get_output(method):
    global method_output
    method_output = {}
    method_output = yaml.load(method.find_all('p')[6].find('pre').string)

def get_responses(method_output):
    responses = method_output.get('responses')
    return responses

def get_pulp_tasks(method_output):
    global pulp_tasks
    pulp_tasks = []
    pulp_tasks.append(method_output.get('pulp_tasks'))

def get_pt_exception(pulp_task):
    exception = pulp_task.get('exception')
    return exception

def get_pt_task_type(pulp_task):
    task_type = pulp_task.get('task_type')
    return task_type

def get_pt_href(pulp_task):
    href = pulp_task.get('_href')
    return href

def get_pt_task_id(pulp_task):
    task_id = pulp_task.get('task_id')
    return task_id

def get_pt_tags(pulp_task):
    tags = pulp_task.get('tags')
    return tags

def get_pt_finish_time(pulp_task):
    finish_time = pulp_task.get('finish_time')
    return finish_time

def get_pt_namespace(pulp_task):
    ns = pulp_task.get('_ns')
    return ns

def get_pt_start_time(pulp_task):
    start_time = pulp_task.get('start_time')
    return start_time

def get_pt_traceback(pulp_task):
    traceback = pulp_task.get('traceback')
    return traceback

def get_pt_spawned_tasks(pulp_task):
    spawned_tasks = pulp_task.get('spawned_tasks')
    return spawned_tasks

def get_pt_progress_report(pulp_task):
    progress_report = pulp_task.get('progress_report')
    return progress_report

def get_pt_queue(pulp_task):
    queue = pulp_task.get('queue')
    return queue

def get_pt_state(pulp_task):
    state = pulp_task.get('state')
    return state

def get_pt_worker_name(pulp_task):
    worker_name = pulp_task.get('worker_name')
    return worker_name

def get_pt_result(pulp_task):
    global result
    result = {}
    result = pulp_task.get('result')
    
def get_result_result(result):
    outcome = result.get('result')
    return outcome

def get_result_repo_id(result):
    repo_id = result.get('repo_id')
    return repo_id

def get_result_started(result):
    started = result.get('started')
    return started

def get_result_namespace(result):
    ns = result.get('_ns')
    return ns

def get_result_completed(result):
    completed = result.get('completed')
    return completed

def get_result_traceback(result):
    traceback = result.get('traceback')
    return traceback

def get_result_distributor_type_id(result):
    dist_type_id = result.get('distributor_type_id')
    return dist_type_id

def get_result_summary(result):
    summary = result.get('summary')
    return summary

def get_result_error_message(result):
    error_message = result.get('error_message')
    return error_message

def get_result_distributor_id(result):
    dist_id = result.get('distributor_id')
    return dist_id

def get_result_id(result):
    id = result.get('id')
    return id

def get_result_details(result):
    details = result.get('details')
    return details

def get_pt_error(pulp_task):
    error = pulp_task.get('error')
    return error

def get_pt_oid(pulp_task):
    oid = pulp_task.get('_id').get('$oid')
    return oid

def get_pt_id(pulp_task):
    id = pulp_task.get('id')
    return id

def get_poll_attempts(method_output):
    poll = method_output.get('poll_attempts')
    return poll

def main(html_file):
    init(html_file)
    get_subtasks(html_file)
    run_tasks = []
    for sequence in get_sequence(sub_tasks):
        for method in get_method(sequence):
            method_dict = {}
            method_dict['label'] = get_label(method)
            method_dict['queue'] = get_method_queue(method)
            method_dict['started_at'] = get_started_at(method)
            method_dict['ended_at'] = get_ended_at(method)
            method_dict['real_time'] = get_real_time(method)
            method_dict['execution_time'] = get_exe_time(method)
            get_input(method)
            method_dict['capsule_id'] = get_capsule_id(method_input)
            if get_repo_id(method_input):
                method_dict['repo_id'] = get_repo_id(method_input)
            else:
                continue
            if get_sync_options(method_input):
                method_dict['sync_options'] = get_sync_options(method_input)
            else:
                continue
            method_dict['remote_user'] = get_remote_user(method_input)
            method_dict['remote_cp_user'] = get_remote_cp_user(method_input)
            method_dict['current_timezone'] = get_current_tz(method_input)
            method_dict['current_user_id'] = get_current_user_id(method_input)
            method_dict['current_organization_id'] = get_current_org_id(method_input)
            method_dict['current_location_id'] = get_current_location_id(method_input)
            method_dict['responses'] = get_responses(method_input)
            get_output(method)
            get_pulp_tasks(method_input)
            if pulp_tasks == []:
                method_dict['pulp_tasks'] = '[]'
            else:
                for element in pulp_tasks:
                    method_dict['exception'] = get_pt_exception(element)
                    method_dict['task_type'] = get_pt_task_type(element)
                    method_dict['href'] = get_pt_href(element)
                    method_dict['task_id'] = get_pt_task_id(element)
                    for tag in get_pt_tags(element):
                        method_dict['pulp:repository'] = tag.get('pulp:repository')
                        method_dict['pulp:action'] = tag.get('pulp:action')
                    method_dict['finish_time'] = get_pt_finish_time(element)
                    method_dict['namespace'] = get_pt_namespace(element)
                    method_dict['start_time'] = get_pt_start_time(element)
                    method_dict['traceback'] = get_pt_traceback(element)
                    for element in get_pt_spawned_tasks(element):
                        method_dict['spawned_task:href'] = get_pt_spawned_tasks(element).get('_href')
                        method_dict['spawned_task:task_id'] = get_pt_spawned_tasks(element).get('task_id')
#This for loop will require some serious inception and time, for another night
#    'progress_report': {'yum_importer': {'content': {'items_total': 0,
#        'state': 'FINISHED',
#        'error_details': [],
#        'details': {'rpm_total': 0,
#        'rpm_done': 0,
#       'drpm_total': 0,
#        'drpm_done': 0},
#        'size_total': 0,
#        'size_left': 0,
#        'items_left': 0},
#    'comps': {'state': 'FINISHED'},
#    'purge_duplicates': {'state': 'FINISHED'},
#    'distribution': {'items_total': 0,
#        'state': 'FINISHED',
#        'error_details': [],
#        'items_left': 0},
#    'modules': {'state': 'FINISHED'},
#    'errata': {'state': 'FINISHED'},
#    'metadata': {'state': 'FINISHED'}}},
                    method_dict['queue'] = get_pt_queue(element)
                    method_dict['state'] = get_pt_state(element)
                    method_dict['worker_name'] = get_pt_worker_name(element)
# More serious coding time
#    'result': {
#        'result': 'success',
#        'importer_id': 'yum_importer',
#        'exception': None,
#        'repo_id': '1-RHEL6_6EUS-SAP-HANA-PROD-733140ea-db53-4460-ad0b-4da889492b1c',
#        'traceback': None,
#        'started': '2020-10-23T18:00:52Z',
#        '_ns': 'repo_sync_results',
#        'completed': '2020-10-23T18:00:59Z',
#        'importer_type_id': 'yum_importer',
#        'error_message': None,
#        'summary': {'modules': {'state': 'FINISHED'},
#        'content': {'state': 'FINISHED'},
#        'comps': {'state': 'FINISHED'},
#        'purge_duplicates': {'state': 'FINISHED'},
#        'distribution': {'state': 'FINISHED'},
#        'errata': {'state': 'FINISHED'},
#        'metadata': {'state': 'FINISHED'}},
#        'added_count': 0,
#        'removed_count': 0,
#        'updated_count': 0,
#       'id': '5f931a5bf60d8e08f3bfcc8e',
#      'details': {'modules': {'state': 'FINISHED'},
#      'content': {'size_total': 0,
#          'items_left': 0,
#            'items_total': 0,
#            'state': 'FINISHED',
#            'size_left': 0,
#            'details': {'rpm_total': 0,
#            'rpm_done': 0,
#            'drpm_total': 0,
#            'drpm_done': 0},
#            'error_details': []},
#        'comps': {'state': 'FINISHED'},
#        'purge_duplicates': {'state': 'FINISHED'},
#        'distribution': {'items_total': 0,
#            'state': 'FINISHED',
#            'error_details': [],
#            'items_left': 0},
#        'errata': {'state': 'FINISHED'},
#        'metadata': {'state': 'FINISHED'}}},
                    method_dict['error'] = get_pt_error(element)
                    method_dict['oid'] = get_pt_oid(element)
                    method_dict['id'] = get_pt_id(element)
                method_dict['poll_attempts'] = get_poll_attempts(method_input)
    run_tasks.append(method_dict)
