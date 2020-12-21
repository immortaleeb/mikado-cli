from mikado.graph.goal import goal_exists
from mikado.graph.project import load_project

def parse_goal_ref_arg(argv, index, mikado_dir):
    if len(argv) > index:
        goal_ref = argv[index]
    else:
        goal_ref = None

    return parse_goal_ref(goal_ref, mikado_dir)

def parse_goal_ref(raw_ref, mikado_dir):
    if raw_ref is None or raw_ref == 'CURRENT':
        return load_project(mikado_dir).current_goal_ref
    elif raw_ref == 'ROOT':
        return load_project(mikado_dir).root_ref
    elif goal_exists(mikado_dir, raw_ref):
        return raw_ref
    else:
        raise Exception("Unknown reference to goal '%s'" % raw_ref)

