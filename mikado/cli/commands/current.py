from mikado.graph.project import load_project

class CurrentCommand:

    @property
    def description(self):
        return "Prints the current goal"

    def run(self, argv):
        project = load_project(self.context.mikado_dir)
        print(project.current_goal_ref)

