from mikado.graph.project import set_current_goal

from mikado.cli.parsing.goal import parse_goal_ref

from .base import AbstractCommand

class SelectCommand(AbstractCommand):

    @property
    def description(self):
        return "Sets the current goal"

    def add_arguments(self, parser):
        parser.add_argument('goal')

    def run(self, args):
        goal_ref = parse_goal_ref(args.goal, self.context.mikado_dir)
        set_current_goal(self.context.mikado_dir, goal_ref)

