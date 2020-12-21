import sys

class HelpCommand:
    def __init__(self, commands):
        self.commands = commands

    @property
    def description(self):
        return "Prints this help"

    def run(self, argv):
        print("Usage: %s [command] [options]" % sys.argv[0])
        print("List of commands:")

        for command_name, command in self.commands.items():
            print("%-10s%s" % (command_name, command.description))

