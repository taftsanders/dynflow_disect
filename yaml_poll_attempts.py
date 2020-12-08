def get_total(poll):
    return poll.get('total')

def get_failed(poll):
    return poll.get('failed')


def main(value):
    polls = []
    polls.append(get_total(value))
    polls.append(get_failed(value))
    return polls