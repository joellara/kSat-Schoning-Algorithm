import re
from random import SystemRandom

def enumerate_variables(formula):
    return re.findall("[A-Z]", formula)


def determine_n(formula):
    return len(set(enumerate_variables(formula)))


def is_well_constructed(formula):
    formula_match = re.match("\(.*?\)(a\(.*?\))*", formula)
    if not formula_match:
        pass
    else:
        clauses = formula_match.group().split("a")
        k = clauses[0].count("o") + 1
        clause_re = re.compile("\((n?[A-Z])(o(n?[A-Z]))*\)")

        for index, clause in enumerate(clauses):
            clause_k = clause.count("o") + 1
            variables = enumerate_variables(clause)
            if not re.match(clause_re, clause) or clause_k != k or len(set(variables)) != len(variables):
                return (False, "Clause {i} is not in a valid form.".format(i=index + 1))
            
        return (True, k)
        
    return (False, "Formula is not in a valid k-conjunctive normal form.")

def determine_formula_attributes(formula):
    (passed, returned) = is_well_constructed(formula)
    if not passed:
        return (passed,returned)
    return (returned, determine_n(formula))




def assign(formula):
    variables = list(set(enumerate_variables(formula)))

    values = {}
    rand = SystemRandom()

    for var in variables:
        rand_val = rand.randint(0,1)
        values[var] = True if rand_val else False

    return values



def evaluate_clause(clause, values):
    variables = enumerate_variables(clause)

    for var in variables:
        var_val = values[var]

        if clause[clause.index(var) - 1] == "n":
            if var_val == False:
                return True
        else:
            if var_val == True:
                return True


    return False




def evaluate_formula(formula, values):
    clauses = formula.split("a")
    false_clause_indexes = []
    formula_is_true = True

    for index, clause in enumerate(clauses):

        if evaluate_clause(clause, values) == False:
            formula_is_true = False
            false_clause_indexes.append(index)

    return (formula_is_true, false_clause_indexes)

def schoning_algo(formula):
    (k, n) = determine_formula_attributes(formula)
    count = 0
    rand = SystemRandom()
    if not k:
        return (False,n)
    while True:
        values = assign(formula)
        count += 1

        for index in xrange(3 * n):
            formula_is_true, false_clause_indexes = evaluate_formula(formula, values)

            if formula_is_true:
                return (values, count)
            else:
                false_clause = formula.split("a")[rand.choice(false_clause_indexes)]
                var_to_change = rand.choice(enumerate_variables(false_clause))
                values[var_to_change] = False if values[var_to_change] == True else True
