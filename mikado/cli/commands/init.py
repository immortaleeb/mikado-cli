import os

from mikado.graph.project import create_project

class InitCommand:
    @property
    def description(self):
        return "Initializes a mikado project"

    def run(self, argv):
        directory = argv[1] if len(argv) > 1 else os.getcwd()

        create_project(directory)

