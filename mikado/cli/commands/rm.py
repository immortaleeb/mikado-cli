from mikado.cli.parsing.goal import parse_goal_ref
from mikado.graph.goal import delete_goal

class RmCommand:

    @property
    def description(self):
        return "Removes the given goal"

    def run(self, argv):
        if len(argv) < 2:
            print('Missing argument: goal ref')
            return 1

        goal_ref = parse_goal_ref(argv[1], self.context.mikado_dir)
        delete_goal(
            mikado_dir=self.context.mikado_dir,
            goal_ref=goal_ref,
        )

