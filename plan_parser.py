from bs4 import BeautifulSoup
import yaml
import yaml_poll_attempts
import yaml_pulp_tasks

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
    label = {}
    for key in action.keys():
        label['label'] = key
    return label

def get_started_at(action):
    started_at = {}
    for value in action.values():
        started_at['started_at'] = value.find_all('p')[0].contents[1].strip()
    return started_at

def get_ended_at(action):
    ended_at = {}
    for value in action.values():
        ended_at['ended_at'] = value.find_all('p')[1].contents[1].strip().split('(')[0].strip()
    return ended_at

def get_input(action):
    action_input = {}
    for value in action.values():
        action_input = yaml.load(value.find_all('p')[2].pre.text, yaml.Loader)
    return action_input

def main(html_file):
    init(html_file)
    plan_actions = []
    for action in get_plan_actions():
        plan_actions.append(get_label(action))
        plan_actions.append(get_started_at(action))
        plan_actions.append(get_ended_at(action))
        for key,value in get_input(action).items():
            if isinstance(value,dict): 
                some_dict = {}
                for key2,value2 in value.items():
                    some_dict[key+'.'+key2] = value2
                plan_actions.append(some_dict)
            elif value is None:
                some_dict = {}
                some_dict[key] = 'None'
                plan_actions.append(some_dict)
            else:
                some_dict = {}
                some_dict[key] = value
                plan_actions.append(some_dict)
    return plan_actions

