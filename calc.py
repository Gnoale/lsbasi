#!/usr/bin/env python3
# Token types
#
# EOF (end-of-file) token is used to indicate that
# there is no more input left for lexical analysis
INTEGER, PLUS, MINUS, PRODUCT, EOF = 'INTEGER', 'PLUS', 'MINUS', 'PRODUCT', 'EOF'


class Token(object):
    def __init__(self, type, value):
        # token type: INTEGER, PLUS, or EOF
        self.type = type
        # token value: 0, 1, 2. 3, 4, 5, 6, 7, 8, 9, '+', or None
        self.value = value

    def __str__(self):
        """String representation of the class instance.

        Examples:
            Token(INTEGER, 3)
            Token(PLUS '+')
        """
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()


class Interpreter(object):
    def __init__(self, text):
        # client string input, e.g. "3+5"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        # current token instance
        self.current_token = None
        self.current_char = self.text[self.pos]
        self.terms = []

    def error(self):
        raise Exception('Error parsing input')

    def advance(self):
        # is self.pos index past the end of the self.text ?
        # if so, then return EOF token because there is no more
        # input left to convert into tokens
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None
            return

        self.current_char = self.text[self.pos]


    def get_number(self):
        num = ""
        while self.current_char != None and self.current_char.isdigit():
            num += self.current_char
            self.advance()
        return int(num)

    def skip_space(self):
        while self.current_char != None and self.current_char.isspace():
            self.advance()


    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.
        """
        text = self.text

        if self.pos > len(text) - 1:
            return Token(EOF, None)

        if self.current_char.isspace():
            self.skip_space()
            return self.get_next_token()

        if self.current_char.isdigit():
            token = Token(INTEGER, self.get_number())
            return token

        if self.current_char == '+':
            token = Token(PLUS, self.current_char)
            self.advance() 
            return token

        if self.current_char == '-':
            token = Token(MINUS, self.current_char)
            self.advance() 
            return token

        if self.current_char == '*':
            token = Token(PRODUCT, self.current_char)
            self.advance() 
            return token

        self.error()

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.get_next_token()
        else:
            self.error()

    def expr(self):
        """expr -> INTEGER PLUS INTEGER"""
        # set current token to the first token taken from the input
        self.current_token = self.get_next_token()

        left = self.current_token
        self.eat(INTEGER)

        op = self.current_token
        self.eat(op.type)

        right = self.current_token
        self.eat(INTEGER)
        # after the above call the self.current_token is set to
        # EOF token


        if op.type == PLUS:
            result = left.value + right.value
        if op.type == MINUS:
            result = left.value - right.value
        if op.type == PRODUCT:
            result = left.value * right.value

        return result
    
    def parse(self):
        self.current_token = self.get_next_token()
        while self.current_token.value != None:
            self.terms.append(self.current_token.value)
            self.eat(self.current_token.type)

def main():
    while True:
        try:
            # To run under Python3 replace 'raw_input' call
            # with 'input'
            text = input('calc> ')
        except EOFError:
            break
        if not text:
            continue
        interpreter = Interpreter(text)
        result = interpreter.expr()
        print(result)


if __name__ == '__main__':
    main()
