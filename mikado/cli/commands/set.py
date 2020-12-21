from .base import AbstractCommand

from mikado.cli.parsing.goal import parse_goal_ref
from mikado.graph.goal import set_status

class SetCommand(AbstractCommand):

    @property
    def description(self):
        return "Sets the status of the given goal"

    def add_arguments(self, parser):
        parser.add_argument('status')
        parser.add_argument('-g', '--goal')

    def run(self, args):
        goal_ref = parse_goal_ref(args.goal, self.context.mikado_dir)
        set_status(
            mikado_dir=self.context.mikado_dir,
            goal_ref=goal_ref,
            new_status=args.status,
        )

