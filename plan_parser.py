from bs4 import BeautifulSoup

def init(html):
    with open(html) as task:
        global soup
        soup = BeautifulSoup(task, 'html.parser')

def get_planned_methods(html):
    init(html)
    methods = soup.body.find_all('ul')
    return methods

def get_method_label(method):
    label = method.span.contents[0]
    return label

def get_started_at(method):
    started_at = method.find_all('p')[1].contents[1]
    return started_at

def get_ended_at(method):
    ended_at = method.find_all('p')[2].contents[1].split('(')[0].strip()
    return ended_at

def get_duration(method):
    duration = method.find_all('p')[2].contents[1].split(' ')[5][:-2]
    return duration

#Not all YAML input is created equal
#Based on label being != 'Class:0x00000000214d6248' type
#Actions::Pulp::Consumer::SyncCapsule
def get_yaml(method):
    yaml = str(method.pre.string).split()
    return yaml

def get_yaml_capsule_id(yaml):
    id = yaml.split()[2]
    return id

def get_yaml_repo_pulp_id(yaml):
    pulp_id = yaml.split()[4]
    return pulp_id

def get_yaml_sync_options(yaml):
    start = yaml.split().index('sync_options:') + 1
    end = yaml.split().index('remote_user:')
    options = []
    while start < end:
        options.append(yaml.split()[start])
        start +=1
    return options

def get_yaml_remote_user(yaml):
    user = yaml.split()[yaml.split().index('remote_user:')+1]
    return user

def get_yaml_remote_cp_user(yaml):
    cp_user = yaml.split()[yaml.split().index('remote_cp_user:')+1]
    return cp_user

def get_yaml_current_timezone(yaml):
    timezone = yaml.split()[yaml.split().index('current_timezone:')+1]
    return timezone

def get_yaml_current_user_id(yaml):
    id = yaml.split()[yaml.split().index('current_user_id:')+1]
    return id

def get_yaml_smart_proxy(yaml):
    start = yaml.split().index('smart_proxy:') + 1
    end = yaml.split().index('services_checked')
    options = []
    while start < end:
        options.append(yaml.split()[start])
        start +=1
    return options

def get_yaml_services_checked(yaml):
    start = yaml.split().index('services_checked:') + 1
    end = yaml.split().index('current_timezone')
    options = []
    while start < end:
        options.append(yaml.split()[start])
        start +=1
    return options

def main(html_file):
    plan = []
    start_index = 1
    while start_index <= len(get_planned_methods(html_file)):
        method_dict = {}
        if get_planned_methods(html_file)[start_index].span.text == '#':
            continue
        else:
            method_dict['label']=get_method_label(html_file)
            method_dict['started_at']=get_started_at(html_file)
            method_dict['ended_at']=get_ended_at(html_file)
            method_dict['duration']=get_duration(html_file)
            method_dict['current_timezone']=get_yaml_current_timezone(html_file)
            method_dict['current_user_id']=get_yaml_current_user_id(html_file)
            if 'smart_proxy:' in get_yaml(html_file):
                method_dict['smart_proxy']=get_yaml_smart_proxy(html_file)
                method_dict['services_checked']=get_yaml_services_checked(html_file)
            else:
                method_dict['capsule_id']=get_yaml_capsule_id(html_file)
                method_dict['repo_pulp_id']=get_yaml_repo_pulp_id(html_file)
                method_dict['sync_options']=get_yaml_sync_options(html_file)
                method_dict['remote_user']=get_yaml_remote_user(html_file)
                method_dict['remote_cp_user']=get_yaml_remote_cp_user(html_file)
        plan.append(method_dict)
        start_index +=1
    return plan