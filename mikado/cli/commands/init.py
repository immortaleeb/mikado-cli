import os

from mikado.graph.project import create_project

from .base import AbstractCommand

class InitCommand(AbstractCommand):
    @property
    def description(self):
        return "Initializes a mikado project"

    def add_arguments(self, parser):
        parser.add_argument('directory', nargs='?', default=os.getcwd())

    def run(self, args):
        create_project(args.directory)

