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

    def as_decimal(self):
        """Convert the item at the top of my stack to decimal."""
        delta = self.stack.pop()
        self.stack.append(delta)
        hours = delta.seconds // 3600
        minutes = (delta.seconds % 3600) // 60
        print("{:.1f}".format(hours + minutes / 60.0))

    def operate(self, operator):
        """Execute operator on the values on my stack."""
        operators = {'+': self.add, '-': self.subtract,}
        y = self.stack.pop()
        x = self.stack.pop()
        result = operators[operator](x, y)
        print(result)
        
    def push(self, value):
        """Push the value onto my stack."""
        h = value[:2]
        m = value[2:]
        self.stack.append(datetime.timedelta(hours=int(h), minutes=int(m)))

    def subtract(self, x, y):
        """Add the two values together pushing the result back on my stack."""
        result = x - y
        self.stack.append(result)
        return result

    def help_dec(self):
        print('Prints item on top of stack in decimal.')
    def do_dec(self, value):
        self.as_decimal()

    def help_done(self):
        print('Quits the program.')
    def do_done(self, line):
        return True

    def help_enter(self):
        print('Enter the next value.')
    def do_enter(self, value):
        self.push(value)

    def help_expr(self):
        print('Enter an (RPN) expression.')
    def do_expr(self, value):
        parts = value.split()
        for part in parts[:-1]:
            self.push(part)
        self.operate(parts[-1])

    def help_exit(self):
        print('Quits the program.')
    def do_exit(self, line):
        return True

    def help_minus(self):
        print('Subtract the two values on the stack.')
    def do_minus(self, args):
        self.operate('-')

    def help_plus(self):
        print('Add the two values on the stack.')
    def do_plus(self, args):
        self.operate('+')

    def precmd(self, line):
        """Convert lines into actual commands."""
        result = line
        parts = line.split()
        if len(parts) > 1:
            result = 'expr {}'.format(line)
        elif len(line) == 4:
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
