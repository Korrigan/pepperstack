"""
Base classes for commands implementation

"""

class CommandMixin(object):
    """
    Base class for implementing commands
    - description will be shown when running `pepper help`
    - help_text will be shown when running `pepper help <command>`
    - cli_mode sets the behavior of the command, if True, the results will be
      printed on the standard output

    When using this base class please take care of the cli_mode attribute

    """
    description = "Pepperstack command"
    help_text = "Pepperstach command long help"
    cli_mode = False


    def __init__(self, cli_mode=False, description=None, help_text=None):
        self.cli_mode = cli_mode
        if description:
            self.description = description
        if help_text:
            self.help_text = help_text


    @classmethod
    def get_description(self):
        """
        A little method if needed for advanced needs

        """
        return self.description

    @classmethod
    def get_help_text(self):
        """
        A little method if needed for advanced needs

        """
        return self.help_text
