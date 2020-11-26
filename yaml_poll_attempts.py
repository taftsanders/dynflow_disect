def get_total(poll):
    return poll.get('total')

def get_failed(poll):
    return poll.get('failed')


def main(value):
    polls = []
    poll = value.get('poll_attempts')
    polls.append(get_total(poll))
    polls.append(get_failed(poll))
    return polls