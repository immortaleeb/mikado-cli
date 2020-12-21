from mikado.graph.goal import Goal

def format_goal(goal):
    status_symbol = format_status_symbol(goal.status)
    return "%s [%s] %s" % (goal.id, status_symbol, goal.title)

def format_status_symbol(status):
    if status == Goal.NEW:
        return ' '
    elif status == Goal.IN_PROGRESS:
        return '~'
    elif status == Goal.DONE:
        return 'X'
    else:
        return '?'

