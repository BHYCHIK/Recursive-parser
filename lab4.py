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
            return [term]
        return None

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
            if self.match('(') is None:
                return None
            simple_expr_res = self.simple_expr()
            if simple_expr_res is None:
                return None
            if self.match(')') is None:
                return None
            return simple_expr_res
        elif self.is_on_top('not'):
            match_not_res = self.match('not')
            if match_not_res is None:
                return None
            factor_res = self.factor()
            if factor_res is None:
                return None
            return factor_res + match_not_res
        return None

    def term_rest(self):
        mul_res = self.op_mul()
        if mul_res is not None:
            factor_res = self.factor()
            if factor_res is None:
                return None
            term_rest_res = self.term_rest()
            if term_rest_res is None:
                return None
            return factor_res + mul_res + term_rest_res
        return []

    def term(self):
        factor_res = self.factor()
        if factor_res is None:
            return None
        term_rest_res = self.term_rest()
        if term_rest_res is None:
            return None
        return factor_res + term_rest_res

    def single_expr_rest(self):
        op_add_res = self.op_add()
        if op_add_res is None:
            return []
        term_res = self.term()
        if term_res is None:
            return None
        single_expr_rest_res = self.single_expr_rest()
        if single_expr_rest_res is None:
            return None
        return term_res + op_add_res + single_expr_rest_res
    
    def simple_expr(self):
        sign_res = self.sign()
        term_res = self.term()
        if term_res is None:
            return None
        signle_expr_rest_res = self.single_expr_rest()
        if signle_expr_rest_res is None:
            return None
        result = term_res
        if sign_res is not None:
            if sign_res[0] == '-':
                result += ['_']
        result += signle_expr_rest_res
        return result

    def expr(self):
        simple_expr_res = self.simple_expr()
        if simple_expr_res is None:
            return None
        res = simple_expr_res
        rel_op_res = self.rel_op()
        if rel_op_res is not None:
            simpl_expr_res2 = self.simple_expr()
            if simpl_expr_res2 is None:
                return None
            res += simpl_expr_res2 + rel_op_res
        return res
    
    def op(self):
        if self.is_identifier_on_top():
            f1 = self.match(self.get_current_terminal())
            if f1 is None:
                return None
            f2 = self.match('=')
            if f2 is None:
                return None
            f3 = self.expr()
            if f3 is None:
                return None
            return f1 + f3 + f2
        return self.block()

    def tail(self):
        if self.is_on_top(';'):
            if self.match(';') is None:
                return None
            f1 = self.op()
            if f1 is None:
                return None
            f2 = self.tail()
            if f2 is None:
                return None
            return f1 + f2
        return []

    def op_list(self):
        op_res = self.op()
        if op_res is None:
            return None
        tail_res = self.tail()
        if tail_res is None:
            return None
        return op_res + tail_res

    def block(self):
        if self.is_on_top('{'):
            if self.match('{') is None:
                return None
            result = self.op_list()
            if self.match('}') is None:
                return None
            return result
        else:
            print 'Block not opened with {'
            return None
    
    def program(self):
        result = self.block()
        if len(self._tokens) != 0:
            print 'Syntax error'
            return None
        return result

input_strings = []
for string in sys.stdin:
    input_strings.append(string)
tokens = ' '.join(input_strings).split()
parser = RecursiveSyntaxParser(tokens)
result = parser.program()
if result is None:
    print 'Error'
else:
    for token in result:
        print token
