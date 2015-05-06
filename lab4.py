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
        if self.get_current_terminal().startswith('id_'):
            return True
        return self.get_current_terminal().isdigit()
 
    def op_mul(self):
        if self.get_current_terminal() in ('*', '/', 'and', 'div', 'mod'):
            return self.match(self.get_current_terminal())

    def op_add(self):
        if self.get_current_terminal() in ('+', '-', 'or'):
            return self.match(self.get_current_terminal())

    def sign(self):
        if self.get_current_terminal() in ('-', '+'):
            return self.match(self.get_current_terminal())

    def rel_op(self):
        if self.get_current_terminal() in ('==', '<>', '<', '<=', '>=', '>'):
            return self.match(self.get_current_terminal())

    def factor(self):
        if self.is_identifier_on_top():
            return self.match(self.get_current_terminal())
        elif self.is_on_top('('):
            return self.match('(') and self.simple_expr() and self.match(')')
        elif self.is_on_top('not'):
            return self.match('not') and self.factor()
        return False

    def term_rest(self):
        if self.op_mul():
            return self.factor() and self.term_rest()
        return True

    def term(self):
        return self.factor() and self.term_rest()

    def single_expr_rest(self):
        if not self.op_add():
            return True
        return self.term() and self.single_expr_rest()
    
    def simple_expr(self):
        self.sign()
        if not self.term():
            return False
        return self.single_expr_rest()

    def expr(self):
        if not self.simple_expr():
            return False
        if self.rel_op():
            return self.simple_expr()
        return True
    
    def op(self):
        if self.is_identifier_on_top():
            result = self.match(self.get_current_terminal()) and self.match('=') and self.expr()
            return result
        return self.block()

    def tail(self):
        if self.is_on_top(';'):
            result = self.match(';') and self.op() and self.tail()
            return result
        return True

    def op_list(self):
        result = self.op() and self.tail()
        return result

    def block(self):
        if self.is_on_top('{'):
            result = self.match('{') and self.op_list() and self.match('}')
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
