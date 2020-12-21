from mikado.graph.project import load_project

from .base import BaseCommand

class CurrentCommand(BaseCommand):

    @property
    def description(self):
        return "Prints the current goal"

    def run(self, args):
        project = load_project(self.context.mikado_dir)
        print(project.current_goal_ref)

