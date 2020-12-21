import os
import argparse

from mikado.graph.project import load_project
from mikado.graph.goal import create_goal

from .base import AbstractCommand

class AddCommand(AbstractCommand):

    @property
    def description(self):
        return "Adds a new goal to the current goal"

    def add_arguments(self, parser):
        parser.add_argument('-t', '--title', required=True)

    def run(self, args):
        project = load_project(self.context.mikado_dir)

        goal_ref = create_goal(
            mikado_dir=self.context.mikado_dir,
            title=args.title,
            description=None,
            parent_ref=project.current_goal_ref,
        )

        print('Goal created with id %s' % goal_ref)

