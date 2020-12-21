from abc import ABC

class AbstractCommand(ABC):

    def add_arguments(self, parser):
        raise NotImplementedError

    def parse(self, args):
        raise NotImplementedError

class BaseCommand(AbstractCommand):

    def add_arguments(self, parser):
        pass

