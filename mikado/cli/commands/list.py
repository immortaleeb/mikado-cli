from mikado.graph.goal import load_goal

from mikado.cli.formatting.goal import format_goal
from mikado.cli.parsing.goal import parse_goal_ref

from .base import AbstractCommand

def print_goal(goal):
    print(format_goal(goal))

class ListCommand(AbstractCommand):

    @property
    def description(self):
        return "Lists all children of the given goal"

    def add_arguments(self, parser):
        parser.add_argument('goal', nargs='?', default=None)

    def run(self, args):
        goal_ref = parse_goal_ref(args.goal, self.context.mikado_dir)

        goal = load_goal(
            mikado_dir=self.context.mikado_dir,
            goal_ref=goal_ref,
        )

        for child in goal.children:
            print_goal(child)

