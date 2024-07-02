from graphviz import Digraph
import os
import base64
from .scanner import Scanner

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.position = 0
        self.current_token = self.tokens[self.position] if self.tokens else None
        self.graph = Digraph(comment='Syntax Tree')

    def advance(self):
        self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None

    def expect(self, expected_type, expected_value=None):
        if self.current_token and self.current_token[0] == expected_type and (expected_value is None or self.current_token[1] == expected_value):
            self.advance()
        else:
            raise SyntaxError(f"Syntax error: expected {expected_type} {expected_value} but got {self.current_token}")

    def parse_expr(self, parent=None):
        expr_node = f'expr{self.position}'
        self.graph.node(expr_node, 'expr')
        if parent:
            self.graph.edge(parent, expr_node)

        self.parse_term(expr_node)
        self.parse_z(expr_node)

        return expr_node

    def parse_z(self, parent=None):
        while self.current_token and self.current_token[1] in ['+', '-']:
            op_node = f'op{self.position}'
            self.graph.node(op_node, self.current_token[1])
            self.graph.edge(parent, op_node)
            self.advance()
            self.parse_expr(op_node)
        return parent

    def parse_term(self, parent=None):
        term_node = f'term{self.position}'
        self.graph.node(term_node, 'term')
        if parent:
            self.graph.edge(parent, term_node)

        self.parse_factor(term_node)
        self.parse_x(term_node)

        return term_node

    def parse_x(self, parent=None):
        while self.current_token and self.current_token[1] in ['*', '/']:
            op_node = f'op{self.position}'
            self.graph.node(op_node, self.current_token[1])
            self.graph.edge(parent, op_node)
            self.advance()
            self.parse_term(op_node)
        return parent

    def parse_factor(self, parent=None):
        factor_node = f'factor{self.position}'
        self.graph.node(factor_node, 'factor')
        if parent:
            self.graph.edge(parent, factor_node)

        if self.current_token and self.current_token[1] == '(':
            self.graph.node(f'paren_open{self.position}', '(')
            self.graph.edge(factor_node, f'paren_open{self.position}')
            self.advance()
            self.parse_expr(factor_node)
            self.expect('SYM', ')')
            self.graph.node(f'paren_close{self.position}', ')')
            self.graph.edge(factor_node, f'paren_close{self.position}')
        elif self.current_token and self.current_token[0] == 'NUM':
            self.graph.node(f'num{self.position}', self.current_token[1])
            self.graph.edge(factor_node, f'num{self.position}')
            self.advance()
        else:
            raise SyntaxError("Syntax error: expected '(', number or identifier")

        return factor_node

    def draw_syntax_tree(self, expression):
        scanner = Scanner(expression)
        self.tokens = scanner.get_tokens()
        self.position = 0
        self.current_token = self.tokens[self.position] if self.tokens else None
        self.parse_expr()
        if not os.path.exists('static'):
            os.makedirs('static')
        file_path = 'static/syntax_tree'
        try:
            self.graph.render(file_path, format='png', cleanup=False)
            with open(f"{file_path}.png", "rb") as image_file:
                return base64.b64encode(image_file.read()).decode('utf-8')
        except Exception as e:
            print(f"Error generating image: {e}")
            return None
