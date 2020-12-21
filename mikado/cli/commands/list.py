from mikado.graph.project import load_project
from mikado.graph.goal import load_goal

from mikado.cli.formatting.goal import format_goal

def print_goal(goal):
    print(format_goal(goal))

class ListCommand:

    @property
    def description(self):
        return "Lists all children of the given goal"

    def run(self, argv):
        project = load_project(self.context.mikado_dir)

        if len(argv) > 1:
            goal_ref = argv[1]
        else:
            goal_ref = project.current_goal_ref

        goal = load_goal(
            mikado_dir=self.context.mikado_dir,
            goal_ref=goal_ref,
        )

        for child in goal.children:
            print_goal(child)

