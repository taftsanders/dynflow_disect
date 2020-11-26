from bs4 import BeautifulSoup
import plan_parser
import yaml
import yaml_pulp_tasks
import yaml_poll_attempts

def init(html_file):
    with open(html_file) as task:
        global soup
        soup = BeautifulSoup(task, 'html.parser')

#Creates a list of dictionaries
# key = plan.label
# value = bs4.element.tag(plan.metadata & plan.input & plan.output)
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
    queue = {}
    for value in action.values():
        queue['queue'] = value
    return queue

def get_real_time(action):
    real_time = {}
    for value in action.values():
        real_time['real_time'] = value.find_all('p')[3].text.split()[2].split('.')[0]
    return real_time

def get_exe_time(action):
    exe_time = {}
    for value in action.values():
        exe_time['execution_time'] = value.find_all('p')[4].text.split(':')[1].split('.')[0].strip()
    return exe_time

def get_input(action):
    action_input = {}
    for value in action.values():
        action_input = yaml.load(value.find_all('p')[5].pre.text)
    return action_input

def get_output(action):
    action_output = {}
    for value in action.values():
        action_output = yaml.load(value.find_all('p')[6].pre.text)
    return action_output

def main(html_file):
    init(html_file)
    run_actions = []
    for action in get_run_actions():
        run_actions.append(plan_parser.get_label(action))
        run_actions.append(get_queue(action))
        run_actions.append(plan_parser.get_started_at(action))
        run_actions.append(plan_parser.get_ended_at(action))
        run_actions.append(get_real_time(action))
        run_actions.append(get_exe_time(action))
        for key,value in get_input(action):
            if isinstance(value,dict): 
                some_dict = {}
                for key2,value2 in value.items():
                    some_dict[key+'.'+key2] = value2
                run_actions.append(some_dict)
            elif value is None:
                some_dict = {}
                some_dict[key] = 'None'
                run_actions.append(some_dict)
            else:
                some_dict = {}
                some_dict[key] = value
                run_actions.append(some_dict)
        for key,value in get_output(action):
            if key == 'pulp_tasks':
                yaml_pulp_tasks.main(value)
            elif key == 'poll_attempts':
                yaml_poll_attempts.main(value)
    return run_actions