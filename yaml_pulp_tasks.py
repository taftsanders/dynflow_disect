''' Lowering scope to get Capsule splicing ready faster
Will focus on getting all data in a future feature

def get_exeception(pulp_task):
    return pulp_task.get('exception')

def get_href(pulp_task):
    return pulp_task.get('_href')

def get_namespace(pulp_task):
    return pulp_task.get('_ns')

def get_traceback(pulp_task):
    return pulp_task.get('traceback')

def get_progress_report(pulp_task):
    return pulp_task.get('progress_report')

def get_pr_puppet_importer(pulp_task):
    return get_progress_report(pulp_task).get('puppet_importer')

def get_pr_pi_modules(pulp_task):
    return get_pr_puppet_importer(pulp_task).get('modules')

def get_pr_pi_mod_error_message(pulp_task):
    return get_pr_pi_modules(pulp_task).get('error_message')

def get_pr_pi_mod_execution_time(pulp_task):
    return get_pr_pi_modules(pulp_task).get('execution_time')
'''
def get_task_type(pulp_task):
    return pulp_task.get('task_type')

def get_task_id(pulp_task):
    return pulp_task.get('task_id')

def get_tags(pulp_task):
    tag_list = []
    tag_list.append({'tag.repo': pulp_task.get('tags')[0]})
    tag_list.append({'tag.action': pulp_task.get('tags')[1]})
    return tag_list

def get_finish_time(pulp_task):
    return pulp_task.get('finish_time')

def get_start_time(pulp_task):
    return pulp_task.get('start_time')


def main(value):
    pulp_tasks = []
    for pulp_task in value:
        pulp_tasks.append(get_task_id(pulp_task))
        pulp_tasks.append(get_task_type(pulp_task))
        for tag in get_tags(pulp_task):
            pulp_tasks.append(tag)
        pulp_tasks.append(get_finish_time(pulp_task))
        pulp_tasks.append(get_start_time(pulp_task))
    return pulp_tasks

