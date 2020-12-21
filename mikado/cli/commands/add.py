import os
import argparse

from mikado.graph.project import load_project
from mikado.graph.goal import create_goal, link_child

from mikado.cli.parsing.goal import parse_goal_ref

from .base import AbstractCommand

class AddCommand(AbstractCommand):

    @property
    def description(self):
        return "Adds a new goal to the current goal"

    def add_arguments(self, parser):
        parser.add_argument('-t', '--title')
        parser.add_argument('-g', '--goal')
        parser.add_argument('-p', '--parent')

    def run(self, args):
        if not (args.title or args.goal):
            print('You should provide either an existing goal or a title for a new goal')
            return 1

        project = load_project(self.context.mikado_dir)
        parent_ref = parse_goal_ref(args.parent, self.context.mikado_dir) if args.parent else project.current_goal_ref

        if args.title:
            goal_ref = create_goal(
                mikado_dir=self.context.mikado_dir,
                title=args.title,
                description=None,
                parent_ref=parent_ref,
            )

            print('Goal created with id %s' % goal_ref)
        elif args.goal:
            project = load_project(self.context.mikado_dir)

            goal_ref = parse_goal_ref(args.goal, self.context.mikado_dir)

            link_child(
                mikado_dir=self.context.mikado_dir,
                parent_ref=parent_ref,
                child_ref=goal_ref,
            )

            print('Goal %s was linked to current goal' % goal_ref)

