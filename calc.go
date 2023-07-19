package main

import (
	"errors"
	"fmt"
	"os"
	"strconv"

	"golang.org/x/term"
)

const (
	EOF     = "EOF"
	INTEGER = "INTEGER"
	PLUS    = "PLUS"
	MULT    = "MULT"
)

type token struct {
	kind  string
	value string
}

type lexeme struct {
	flow    string
	tokens  []token
	pointer int
}

func (t token) String() string {
	return fmt.Sprintf("Token %v = %v", t.kind, t.value)
}

func newToken(c string) (token, error) {
	_, err := strconv.Atoi(c)
	if err != nil {
		switch c {
		case "+":
			return token{"PLUS", "+"}, nil
		case "*":
			return token{"MULT", "*"}, nil
		}
	} else {
		return token{"INTEGER", c}, nil
	}
	return token{}, errors.New(fmt.Sprintf("invalid char [%v] ,unable to get a new token", c))
}

func (l *lexeme) isInteger(integer string) (token, error) {
	var err error
	fmt.Println("fuuck")
	for l.pointer < len(l.flow)-1 && err == nil {
		nextChar := string(l.flow[l.pointer+1])
		if _, err = strconv.Atoi(nextChar); err == nil {
			integer += nextChar
		}
		l.pointer += 1
	}
	return newToken(integer)
}

func (l *lexeme) skipSpace() {
	for l.pointer < len(l.flow) && string(l.flow[l.pointer]) == " " {
		l.pointer += 1
	}
}

func (l *lexeme) getNextToken() (token, error) {

	if l.pointer == len(l.flow) {
		return token{"EOF", ""}, nil
	}

	l.skipSpace()
	currentChar := string(l.flow[l.pointer])

	if _, err := strconv.Atoi(currentChar); err == nil {
		return l.isInteger(currentChar)
	}

	token, err := newToken(currentChar)
	l.pointer += 1
	return token, err
}

func (l *lexeme) express() {
	currentToken, err := l.getNextToken()

	for currentToken.kind != EOF && err == nil {
		l.tokens = append(l.tokens, currentToken)
		currentToken, err = l.getNextToken()
	}

	if err != nil {
		panic(err)
	}
	return
}

func main() {

	terminal := term.NewTerminal(os.Stdin, "> ")

	state, _ := term.MakeRaw(int(os.Stdin.Fd()))
	defer term.Restore(int(os.Stdin.Fd()), state)

	for {
		line, _ := terminal.ReadLine()
		lex := &lexeme{
			line,
			make([]token, 0),
			0,
		}

		lex.express()
		fmt.Println(lex.tokens)
		//terminal.SetPrompt("> ")
	}

}
