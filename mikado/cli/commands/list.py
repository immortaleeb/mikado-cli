from mikado.graph.goal import load_goal

from mikado.cli.formatting.goal import format_goal
from mikado.cli.parsing.goal import parse_goal_ref_arg

def print_goal(goal):
    print(format_goal(goal))

class ListCommand:

    @property
    def description(self):
        return "Lists all children of the given goal"

    def run(self, argv):
        goal_ref = parse_goal_ref_arg(argv, 1, self.context.mikado_dir)

        goal = load_goal(
            mikado_dir=self.context.mikado_dir,
            goal_ref=goal_ref,
        )

        for child in goal.children:
            print_goal(child)

