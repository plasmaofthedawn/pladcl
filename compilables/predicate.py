from ast import Not
from .compilable import Compilable, CompileError, Expression, Parameter, join_compilables, register_class
from util import unwrap_singleton

COMPARISON_INVERSE_MAP = {
    "=": "!=",
    "==": "!=",
    "!=": "=",
    ">": "!>",
    ">=": "<",
    "<": "!<",
    "<=": ">",
    "!<": "<",
    "!>": ">",
}

COMPARISON_MAP = {
    "=": "=",
    "==": "=",
    "!=": "!=",
    ">": ">",
    ">=": "!<",
    "<": "<",
    "<=": "!>",
    "!<": "!<",
    "!>": "!>",
}


class Predicate(Compilable, Parameter):

    @classmethod
    def from_tree(cls, tree):

        parse = cls.parse_tree(tree, process_types=False)

        if "AND" in parse:
            return PredicateAnd.from_tree(tree)

        if "OR" in parse:
            return PredicateOr.from_tree(tree)

        if "NOT" in parse:
            return PredicateNot.from_tree(tree)

        if "COMPARISONS" in parse:
            return PredicateBase.from_tree(tree)

        return cls.from_tree(unwrap_singleton(tree))

    def compile(self, globals):
            
        #print(self)
        pred = self.de_morgans()
        #print(pred)
        pred = pred.distribute()
        #print(pred)
        flat = pred.flatten()

        # extra wrapping just in case
        if isinstance(pred, PredicateAnd):
            flat = [flat]
        if isinstance(pred, PredicateBase):
            return pred.compile(globals)

        out = "0" # start the sum
        for ors in flat:
            out += "[" # start this or chain
            for p in ors:
                out += (~p).compile(globals)
                out += "q" # quit if not this 
            out += "1+]x" # otherwise inc

        out += "0!="

        return out 
        
    def r_compile(self, globals):

       return (~self).compile(globals) 

    def de_morgans(self) -> "Predicate":
        raise NotImplemented

    def distribute(self) -> "Predicate":
        raise NotImplemented

    def __invert__(self) -> "Predicate":
        return PredicateNot.from_kwargs(pred=self)

register_class(Predicate, "predicate")


class PredicateAnd(Predicate):

    pred1: Predicate
    pred2: Predicate

    def de_morgans(self):
        return PredicateOr.from_kwargs(pred1=self.pred1.de_morgans(), pred2=self.pred2.de_morgans())

    def distribute(self):
        if isinstance(self.pred1, PredicateOr): 
            return PredicateOr.from_kwargs(
                    pred1=PredicateAnd.from_kwargs(pred1=self.pred1.pred1, pred2=self.pred2),
                    pred2=PredicateAnd.from_kwargs(pred1=self.pred1.pred2, pred2=self.pred2)
            ).distribute()
        if isinstance(self.pred2, PredicateOr):
            return PredicateOr.from_kwargs(
                    pred1=PredicateAnd.from_kwargs(pred1=self.pred1, pred2=self.pred2.pred1),
                    pred2=PredicateAnd.from_kwargs(pred1=self.pred1, pred2=self.pred2.pred2)
            ).distribute()

        out = PredicateAnd.from_kwargs(pred1=self.pred1.distribute(), pred2=self.pred2.distribute())
        if out.contains_or():
            return out.distribute()
        return out

    def contains_or(self):

        def t(p):
            if isinstance(p, PredicateOr):
                return True 
            elif isinstance(p, PredicateAnd):
                return p.contains_or()
            return False

        return t(self.pred1) or t(self.pred2)

    def flatten(self):
        out = []

        for p in [self.pred1, self.pred2]:
            if isinstance(p, PredicateOr):
                raise self.error("Something went wrong in predicate cnf logic")
            elif isinstance(p, PredicateAnd):
                out.extend(p.flatten())
            else:
                out.append(p)

        return out

    @classmethod
    def from_tree(cls, tree):
        c = super(Predicate, cls).from_tree(tree)

        parse = cls.parse_tree(tree)

        c.pred1 = parse["predicate"][0]
        c.pred2 = parse["predicate"][1]

        return c

    def __str__(self):
        return f"({self.pred1} and {self.pred2})"



class PredicateOr(Predicate):
    pred1: Predicate
    pred2: Predicate    

    def de_morgans(self):
        return PredicateOr.from_kwargs(pred1=self.pred1.de_morgans(), pred2=self.pred2.de_morgans())

    def distribute(self):
        return PredicateOr.from_kwargs(pred1=self.pred1.distribute(), pred2=self.pred2.distribute())

    def flatten(self):
        out = []

        for p in [self.pred1, self.pred2]:
            if isinstance(p, PredicateOr):
                out.extend(p.flatten())
            elif isinstance(p, PredicateAnd):
                out.append(p.flatten())
            else:
                out.append([p])

        return out

    @classmethod
    def from_tree(cls, tree):
        c = super(Predicate, cls).from_tree(tree)

        parse = cls.parse_tree(tree)

        c.pred1 = parse["predicate"][0]
        c.pred2 = parse["predicate"][1]

        return c

    def __str__(self):
        return f"({self.pred1} or {self.pred2})"



class PredicateNot(Predicate):
    pred: Predicate

    def de_morgans(self):
        if isinstance(self.pred, PredicateBase):
            return ~self.pred
        elif isinstance(self.pred, PredicateNot):
            return self.pred.pred
        elif isinstance(self.pred, PredicateOr):
            return PredicateAnd.from_kwargs(
                        pred1=PredicateNot.from_kwargs(pred=self.pred.pred1).de_morgans(),
                        pred2=PredicateNot.from_kwargs(pred=self.pred.pred2).de_morgans(),
            )
        elif isinstance(self.pred, PredicateAnd):
            return PredicateOr.from_kwargs(
                        pred1=PredicateNot.from_kwargs(pred=self.pred.pred1).de_morgans(),
                        pred2=PredicateNot.from_kwargs(pred=self.pred.pred2).de_morgans(),
            )

        return PredicateNot.from_kwargs(pred=self.pred)

    def flatten(self):
        raise self.error("not was flattened -- bug in predicate cnf logic")

    @classmethod
    def from_tree(cls, tree):
        c = super(Predicate, cls).from_tree(tree)

        parse = cls.parse_tree(tree)

        c.pred = parse["predicate"][0]

        return c
    
    def __str__(self):
        return f"(not {self.pred})"



class PredicateBase(Predicate):
    param1: Expression
    param2: Expression
    comparison: str

    def de_morgans(self):
        return PredicateBase.from_kwargs(param1=self.param1, param2=self.param2, comparison=self.comparison)

    def flatten(self):
        return PredicateBase.from_kwargs(param1=self.param1, param2=self.param2, comparison=self.comparison)

    def distribute(self):
        return self 

    def __invert__(self):
        return PredicateBase.from_kwargs(param1=self.param1, param2=self.param2, comparison=COMPARISON_INVERSE_MAP[self.comparison])

    @classmethod
    def from_tree(cls, tree):
        c = super(Predicate, cls).from_tree(tree)
        
        parse = cls.parse_tree(tree)

        c.param1 = parse["expression"][0]
        c.param2 = parse["expression"][1]
        c.comparison = parse["COMPARISONS"][0].getText()

        return c

    def compile(self, globals):
        return f"{join_compilables((self.param2, self.param1), globals)}{COMPARISON_MAP[self.comparison]}"


    def __str__(self):
        return f"({self.param1} {self.comparison} {self.param2})"

    def __repr__(self):
        return str(self)

