from mikado.graph.project import set_current_goal

from mikado.cli.parsing.goal import parse_goal_ref

class SelectCommand:

    @property
    def description(self):
        return "Sets the current goal"

    def run(self, argv):
        if len(argv) < 2:
            print('Missing argument: new goal')
            return 1

        goal_ref = parse_goal_ref(argv[1], self.context.mikado_dir)
        set_current_goal(self.context.mikado_dir, goal_ref)

