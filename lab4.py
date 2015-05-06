import sys
class RecursiveSyntaxParser(object):
    def __init__(self, tokens):
        self._tokens = tokens[:]
        self._result = []

    def get_current_terminal(self):
        return self._tokens[0]

    def is_on_top(self, term):
        return self.get_current_terminal() == term

    def remove_top_token(self):
        self._tokens = self._tokens[1:]

    def match(self, term):
        if self.is_on_top(term):
            self.remove_top_token()
            return True
        return False

    def is_identifier_on_top(self):
        return self.get_current_terminal().startswith('id_')

    def expr(self):
        return self.match('4')
    
    def op(self):
        if self.is_identifier_on_top():
            result = self.match(self.get_current_terminal()) and self.match('=') and self.expr()
            return result
        return self.block()

    def tail(self):
        if self.is_on_top(';'):
            result = self.match(';') and self.op() and self.tail()
        return True

    def op_list(self):
        result = self.op() and self.tail()
        return result

    def block(self):
        if self.is_on_top('{'):
            result = self.match('{') and self.op_list() and self.match('}')
            print 'BLOCK RESULT %s' % result
            return result
        else:
            print 'Block not opened with {'
            return False
    
    def program(self):
        result = self.block()
        if len(self._tokens) != 0:
            print 'Syntax error'
            return False
        return result

input_strings = []
for string in sys.stdin:
    input_strings.append(string)
tokens = ' '.join(input_strings).split()
parser = RecursiveSyntaxParser(tokens)
result = parser.program()
print parser._tokens
print result
