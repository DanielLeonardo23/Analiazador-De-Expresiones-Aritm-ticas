class Scanner:
    def __init__(self, input_string):
        self.tokens = input_string.replace(' ', '')
        self.position = 0
        self.current_token = self.tokens[self.position] if self.tokens else None

    def advance(self):
        self.position += 1
        self.current_token = self.tokens[self.position] if self.position < len(self.tokens) else None

    def get_tokens(self):
        tokens = []
        while self.current_token is not None:
            if self.current_token.isdigit():
                tokens.append(('NUM', self.current_token))
            elif self.current_token.isalpha():
                tokens.append(('ID', self.current_token))
            elif self.current_token in '+-*/()':
                tokens.append(('SYM', self.current_token))
            self.advance()
        return tokens
