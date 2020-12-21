from mikado.graph.goal import load_goal

from mikado.cli.formatting.goal import format_goal
from mikado.cli.parsing.goal import parse_goal_ref

from .base import AbstractCommand

def print_goal(goal, is_visited, depth=0):
    if depth == 0:
        prefix = '.'
    else:
        prefix = '|--' if len(goal.children_refs) < 1 else '|-+'

        if is_visited:
            prefix += ' (*)'

    whitespace = ' ' * depth * 2
    print(whitespace + prefix + ' ' + format_goal(goal))

def print_tree(goal, visited, depth=0):
    is_visited = goal.id in visited

    print_goal(goal, is_visited, depth)

    if not is_visited:
        visited.append(goal.id)

        for child in goal.children:
            print_tree(child, visited, depth+1)

class TreeCommand(AbstractCommand):

    @property
    def description(self):
        return "Prints a tree of the given goal"

    def add_arguments(self, parser):
        parser.add_argument('goal', nargs='?', default=None)

    def run(self, args):
        goal_ref = parse_goal_ref(args.goal, self.context.mikado_dir)

        root_goal = load_goal(
            mikado_dir=self.context.mikado_dir,
            goal_ref=goal_ref,
        )

        print_tree(root_goal, [])

