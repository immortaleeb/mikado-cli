from mikado.cli.parsing.goal import parse_goal_ref
from mikado.graph.goal import delete_goal

from .base import AbstractCommand

class RmCommand(AbstractCommand):

    @property
    def description(self):
        return "Removes the given goal"

    def add_arguments(self, parser):
        parser.add_argument('goal')

    def run(self, args):
        goal_ref = parse_goal_ref(args.goal, self.context.mikado_dir)
        delete_goal(
            mikado_dir=self.context.mikado_dir,
            goal_ref=goal_ref,
        )

