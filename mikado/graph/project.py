import os
from pathlib import Path

from .goal import load_goal, create_goal, goal_exists

DEFAULT_MIKADO_DIR = os.path.join(os.getcwd(), '.mikado')

def set_current_goal(mikado_dir, goal_ref):
    if not goal_exists(mikado_dir, goal_ref):
        raise Exception("Unknown goal with id '%s'" % goal_ref)

    set_current_file(mikado_dir, goal_ref)

def set_current_file(mikado_dir, goal_ref):
    current_file = os.path.join(mikado_dir, 'CURRENT')

    with open(current_file, 'w+') as f:
        f.write(goal_ref + '\n')

def load_current_file(mikado_dir):
    current_file = os.path.join(mikado_dir, 'CURRENT')

    with open(current_file, 'r') as f:
        return f.read().strip()

def create_root_goal(mikado_dir):
    return create_goal(
        mikado_dir=mikado_dir,
        title='root',
        description=None,
    )

def create_project_file(mikado_dir, root_id):
    root_file = os.path.join(mikado_dir, 'PROJECT')

    with open(root_file, 'w+') as f:
        f.write('root: %s\n' % root_id)

def load_project_file(mikado_dir):
    project_data = {}

    project_file = os.path.join(mikado_dir, 'PROJECT')
    with open(project_file, 'r+') as f:
        for line in f.readlines():
            stripped_line = line.strip()
            if stripped_line:
                if stripped_line.startswith('root: '):
                    project_data['root_ref'] = stripped_line.replace('root: ', '')
                else:
                    print("WARNING: Got unknown line while parsing PROJECT file: '%s'", line)

    return project_data

def create_project(directory):
    if not os.path.exists(directory):
        raise Exception("Path '%s' does not exist" % directory)

    if not os.path.isdir(directory):
        raise Exception("Path '%s' is not a valid directory" % directory)

    mikado_dir = os.path.join(directory, '.mikado')

    if os.path.exists(mikado_dir):
        raise Exception("Path '%s' is already a mikado project" % directory)

    try:
        os.mkdir(mikado_dir)
        os.mkdir(os.path.join(mikado_dir, 'objects'))

        root_id = create_root_goal(mikado_dir)
        create_project_file(mikado_dir, root_id)
        set_current_goal(mikado_dir, root_id)
    except:
        print("Could not initialize mikado project in directory %s" % directory)
        raise
    else:
        print("Initialized mikado project in directory %s" % directory)

def load_project(mikado_dir):

    project_data = {
        'mikado_dir': mikado_dir,
        **load_project_file(mikado_dir),
        'current_goal_ref': load_current_file(mikado_dir),
    }

    return Project(**project_data)


class Project:

    def __init__(self, *, mikado_dir, root_ref, current_goal_ref):
        self.mikado_dir = mikado_dir
        self.root_ref = root_ref
        self.current_goal_ref = current_goal_ref

    @property
    def current_goal(self):
        return self._load_goal(self.current_goal_ref)

    @property
    def root(self):
        return self._load_goal(self.root_ref)

    @property
    def goals(self):
        for goal in self.root.children:
            yield goal

    # helper methods
    def _load_goal(self, goal_ref):
        return load_goal(
            mikado_dir=self.mikado_dir,
            goal_ref=goal_ref,
        )

