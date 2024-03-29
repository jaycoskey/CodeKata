#!/usr/bin/env python

from abc import ABC
import operator


def binop(op, op_token):
    def modified(cls):
        def __init__(self, x, y):
            self.x = x
            self.y = y

        def __str__(self):
            return self.x.__str__() + op_token + self.y.__str__()

        def fmap(self, f):
            return cls(f(self.x), f(self.y))

        def evaluation(self):
            return op(self.x.evaluation()
                          if issubclass(type(self.x), Expr)
                          else self.x
                    , self.y.evaluation()
                          if issubclass(type(self.y), Expr)
                          else self.y)
        setattr(cls, '__init__', __init__)
        setattr(cls, '__str__', __str__)
        setattr(cls, 'fmap', fmap)
        setattr(cls, 'evaluation', evaluation)
        return cls

    return modified


class Expr(ABC):
    # Compare with the fixed-point combinator.
    def cata(self, f):
        cata_f = lambda x: x.cata(f)
        fmapped = self.fmap(cata_f)
        return f(fmapped)

    def eval_with(self, f):
        return self.cata(f)


class ExprConst(Expr):
    def __init__(self, x):
        self.x = x
    def __str__(self):
        return self.x.__str__()
    def fmap(self, f):
        return self
    def evaluation(self):
        return self.x


@binop(operator.add, '+')
class ExprAdd(Expr):
    pass


@binop(operator.truediv, '/')
class ExprDiv(Expr):
    pass


@binop(operator.mul, '*')
class ExprMul(Expr):
    pass


@binop(operator.sub, '-')
class ExprSub(Expr):
    pass


setattr(Expr, '__add__',     lambda self, other: ExprAdd(self, other))
setattr(Expr, '__truediv__', lambda self, other: ExprDiv(self, other))
setattr(Expr, '__mul__',     lambda self, other: ExprMul(self, other))
setattr(Expr, '__sub__',     lambda self, other: ExprSub(self, other))


def evaluate(expr):
    return expr.evaluation()


def expr_eval_demo():
    one = ExprConst(1)
    two = ExprConst(2)
    three = ExprConst(3)
    four = ExprConst(4)
    x = one + two * three / four
    x_str = x.eval_with(str)
    x_val = x.eval_with(evaluate)
    print(f'Expression as string: {x_str}')
    print(f'Expression evaluated: {x_val}')


if __name__ == '__main__':
    expr_eval_demo()
