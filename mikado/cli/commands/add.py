import os

from mikado.graph.project import load_project
from mikado.graph.goal import create_goal

class AddCommand:

    @property
    def description(self):
        return "Adds a new goal to the current goal"

    def run(self, argv):
        if len(argv) < 2:
            print('Missing title argument')
            return 1

        project = load_project(self.context.mikado_dir)

        goal_ref = create_goal(
            mikado_dir=self.context.mikado_dir,
            title=argv[1],
            description=None,
            parent_ref=project.current_goal_ref,
        )

        print('Goal created with id %s' % goal_ref)

