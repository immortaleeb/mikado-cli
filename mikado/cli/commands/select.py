from mikado.graph.project import set_current_goal

class SelectCommand:

    @property
    def description(self):
        return "Sets the current goal"

    def run(self, argv):
        if len(argv) < 2:
            print('Missing argument: new goal')
            return 1

        set_current_goal(self.context.mikado_dir, argv[1])

