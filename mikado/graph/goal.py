import os
import uuid

loaded_goals = {}

def generate_id():
    return str(uuid.uuid4())

def goal_exists(mikado_dir, goal_ref):
    goal_file = os.path.join(mikado_dir, 'objects', goal_ref)

    return os.path.isfile(goal_file)

def load_goal(*, mikado_dir, goal_ref):
    if goal_ref in loaded_goals:
        return loaded_goals[goal_ref]

    goal_file = os.path.join(mikado_dir, 'objects', goal_ref)

    goal_data = {
        'id': goal_ref,
        'status': Goal.NEW,
        'parent_refs': [],
        'children_refs': [],
        'mikado_dir': mikado_dir,
    }

    with open(goal_file, 'r') as f:
        for line in f.readlines():
            if line.strip():
                if line.startswith('title:'):
                    goal_data['title'] = line.replace('title:', '').strip()
                elif line.startswith('description:'):
                    goal_data['description'] = line.replace('description:', '').strip()
                elif line.startswith('child:'):
                    child_ref = line.replace('child:', '').strip()
                    goal_data['children_refs'].append(child_ref)
                elif line.startswith('parent:'):
                    parent_ref = line.replace('parent:', '').strip()
                    goal_data['parent_refs'].append(parent_ref)
                elif line.startswith('status:'):
                    goal_data['status'] = line.replace('status:', '').strip()

    goal = Goal(**goal_data)
    loaded_goals[goal_ref] = goal

    return goal

def link_child(*, mikado_dir, parent_ref, child_ref):
    if is_offspring(
        mikado_dir=mikado_dir,
        parent_ref=child_ref,
        child_ref=parent_ref,
    ):
        raise Exception("Possible cycle detected, cannot link goals")

    parent_file = os.path.join(mikado_dir, 'objects', parent_ref)

    with open(parent_file, 'a') as f:
        f.write('child: %s\n' % child_ref)

    child_file = os.path.join(mikado_dir, 'objects', child_ref)

    with open(child_file, 'a') as f:
        f.write('parent: %s\n' % parent_ref)

def unlink_child(*, mikado_dir, parent_ref, child_ref):
    parent_file = os.path.join(mikado_dir, 'objects', parent_ref)
    _remove_line(parent_file, lambda line: line.strip() == 'child: ' + child_ref)

    child_file = os.path.join(mikado_dir, 'objects', child_ref)
    _remove_line(child_file, lambda line: line.strip() == 'parent: ' + parent_ref)

def _remove_line(goal_file, match_func):
    _replace_line(goal_file, match_func, None)

def _replace_line(goal_file, match_func, replacement):
    with open(goal_file, 'r') as f:
        lines = f.readlines()

    with open(goal_file, 'w') as f:
        for line in lines:
            if match_func(line):
                if replacement:
                    f.write(replacement + '\n')
            else:
                f.write(line)

def create_goal(*, mikado_dir, title, description, parent_ref=None):
    id = generate_id()

    goal_file = os.path.join(mikado_dir, 'objects', id)

    with open(goal_file, 'w+') as f:
        f.write("title: %s\n" % title)
        f.write("description: %s\n" % (description or ''))
        f.write("status: %s\n" % Goal.NEW)

    if parent_ref:
        link_child(mikado_dir=mikado_dir, parent_ref=parent_ref, child_ref=id)

    return id

def delete_goal(*, mikado_dir, goal_ref):
    goal = load_goal(
        mikado_dir=mikado_dir,
        goal_ref=goal_ref,
    )

    for parent_ref in goal.parent_refs:
        unlink_child(
            mikado_dir=mikado_dir,
            parent_ref=parent_ref,
            child_ref=goal_ref,
        )

def is_offspring(*, mikado_dir, parent_ref, child_ref):
    if parent_ref == child_ref:
        return True

    child = load_goal(
        mikado_dir=mikado_dir,
        goal_ref=child_ref,
    )

    for parent in child.parents:
        if is_offspring(
            mikado_dir=mikado_dir,
            parent_ref=parent_ref,
            child_ref=parent.id,
        ):
            return True

    return False

def set_status(*, mikado_dir, goal_ref, new_status):
   goal_file = os.path.join(mikado_dir, 'objects', goal_ref)

   _replace_line(goal_file, lambda line: line.startswith('status:'), 'status: ' + new_status)

class Goal:

    NEW = 'new'
    IN_PROGRESS = 'in_progress'
    DONE = 'done'

    def __init__(self, *, mikado_dir, id, title, description, status, parent_refs, children_refs):
        self.id = id
        self.title = title
        self.description = description
        self.status = status

        self.parent_refs = parent_refs
        self.children_refs = children_refs

        self.mikado_dir = mikado_dir

    @property
    def parents(self):
        for parent_ref in self.parent_refs:
            yield load_goal(
                mikado_dir=self.mikado_dir,
                goal_ref=parent_ref,
            )

    @property
    def children(self):
        for child_ref in self.children_refs:
            yield load_goal(
                mikado_dir=self.mikado_dir,
                goal_ref=child_ref,
            )

