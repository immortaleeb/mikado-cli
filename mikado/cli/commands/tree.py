from mikado.graph.goal import load_goal

from mikado.cli.formatting.goal import format_goal
from mikado.cli.parsing.goal import parse_goal_ref_arg

def print_goal(goal, depth=0):
    if depth == 0:
        prefix = '.'
    else:
        prefix = '|--' if len(goal.children_refs) < 1 else '|-+'

    whitespace = ' ' * depth * 2
    print(whitespace + prefix + ' ' + format_goal(goal))

def print_tree(goal, depth=0):
    print_goal(goal, depth)

    for child in goal.children:
        print_tree(child, depth+1)

class TreeCommand:

    @property
    def description(self):
        return "Prints a tree of the given goal"

    def run(self, argv):
        goal_ref = parse_goal_ref_arg(argv, 1, self.context.mikado_dir)

        root_goal = load_goal(
            mikado_dir=self.context.mikado_dir,
            goal_ref=goal_ref,
        )

        print_tree(root_goal)
