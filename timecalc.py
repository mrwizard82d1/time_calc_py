"""Implements a time calculator."""


import cmd
import datetime


class TimeCalculator(cmd.Cmd):
    """Time calculator (command-line) application."""

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'time_calc: '
        self.intro = 'Welcome to the RPN time calculator!'
        self.stack = []

    def add(self, x, y):
        """Add the two values together pushing the result back on my stack."""
        result = x + y
        self.stack.append(result)
        return result

    def subtract(self, x, y):
        """Add the two values together pushing the result back on my stack."""
        result = x - y
        self.stack.append(result)
        return result

    def help_done(self):
        print('quits the program')
    def do_done(self, line):
        return True

    def help_enter(self):
        print('Enter the next value.')
    def do_enter(self, value):
        h = value[:2]
        m = value[2:]
        self.stack.append(datetime.timedelta(hours=int(h), minutes=int(m)))

    def help_minus(self):
        print('Subtract the two values on the stack.')
    def do_minus(self, args):
        y = self.stack.pop()
        x = self.stack.pop()
        result = self.subtract(x, y)
        print(result)

    def help_plus(self):
        print('Add the two values on the stack.')
    def do_plus(self, args):
        y = self.stack.pop()
        x = self.stack.pop()
        result = self.add(x, y)
        print(result)

    def precmd(self, line):
        """Convert lines into actual commands."""
        result = line
        if len(line) == 4:
            try:
                int(line)
                result = 'enter {}'.format(line)
            except ValueError:
                pass
        elif len(line) == 1:
            if line == '+':
                result = 'plus'
            elif line == '-':
                result = 'minus'
        return result

    
def main():
    """Driver for application."""
    app = TimeCalculator()
    app.cmdloop()


if __name__ == '__main__':
    main()
