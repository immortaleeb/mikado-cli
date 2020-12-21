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
        return goal_ref

    goal_file = os.path.join(mikado_dir, 'objects', goal_ref)

    goal_data = {
        'id': goal_ref,
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

    goal = Goal(**goal_data)
    loaded_goals[goal_ref] = goal

    return goal

def link_child(*, mikado_dir, parent_ref, child_ref):
    parent_file = os.path.join(mikado_dir, 'objects', parent_ref)

    with open(parent_file, 'a') as f:
        f.write('child: %s\n' % child_ref)

    child_file = os.path.join(mikado_dir, 'objects', child_ref)

    with open(child_file, 'a') as f:
        f.write('parent: %s\n' % parent_ref)

def unlink_child(*, mikado_dir, parent_ref, child_ref):
    parent_file = os.path.join(mikado_dir, 'objects', parent_ref)

    with open(parent_file, 'r') as f:
        parent_lines = f.readlines()

    with open(parent_file, 'w') as f:
        for line in parent_lines:
            if line.strip() != 'child: ' + child_ref:
                f.write(line)

    child_file = os.path.join(mikado_dir, 'objects', child_ref)

    with open(child_file, 'r') as f:
        child_lines = f.readlines()

    with open(child_file, 'w') as f:
        for line in child_lines:
            if line.strip() != 'parent: ' + parent_ref:
                f.write(line)

def create_goal(*, mikado_dir, title, description, parent_ref=None):
    id = generate_id()

    goal_file = os.path.join(mikado_dir, 'objects', id)

    with open(goal_file, 'w+') as f:
        f.write("title: %s\n" % title)
        f.write("description: %s\n" % (description or ''))

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

class Goal:

    def __init__(self, *, mikado_dir, id, title, description, parent_refs, children_refs):
        self.id = id
        self.title = title
        self.description = description
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

