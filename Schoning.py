import re
import random

def num_variables(formula):
    return re.findall("[A-Z]", formula)


def determine_n(formula):
    return len(set(num_variables(formula)))


def check_valid(formula):
    formula_match = re.match("\(.*?\)(a\(.*?\))*", formula)
    if not formula_match:
        pass
    else:
        clauses = formula_match.group().split("a")
        k = clauses[0].count("o") + 1
        clause_re = re.compile("\((n?[A-Z])(o(n?[A-Z]))*\)")

        for index, clause in enumerate(clauses):
            clause_k = clause.count("o") + 1
            variables = num_variables(clause)
            if not re.match(clause_re, clause) or clause_k != k or len(set(variables)) != len(variables):
                return (False, "La clausula {i} no tiene formato valido.".format(i=index + 1))

        return (True, k)

    return (False, "Formula no tiene forma valida conjuntiva normal.")

def check_getn(formula):
    (passed, returned) = check_valid(formula)
    if not passed:
        return (passed,returned)
    return (returned, determine_n(formula))




def assign(formula):
    variables = list(set(num_variables(formula)))
    values = {}
    for var in variables:
        values[var] = random.choice([False,True])
    return values



def check_clause(clause, values):
    variables = num_variables(clause)

    for var in variables:
        var_val = values[var]

        if clause[clause.index(var) - 1] == "n":
            if  not var_val:
                return True
        else:
            if var_val:
                return True
    return False




def check_solution(formula, values):
    clauses = formula.split("a")
    failed = []
    satisfied = True

    for index, clause in enumerate(clauses):

        if not check_clause(clause, values):
            satisfied = False
            failed.append(index)

    return (satisfied, failed)

def schoning_algo(formula):
    (k, n) = check_getn(formula)
    count = 0
    if not k:
        return (False,n)
    values = assign(formula)
    for index in xrange(3 * n):
        count += 1
        satisfied, failed = check_solution(formula, values)
        if satisfied:
            return (values, count)
        else:
            false_clause = formula.split("a")[random.choice(failed)]
            var_to_change = random.choice(num_variables(false_clause))
            values[var_to_change] = False if values[var_to_change]  else True
    return (False,"No se encontro solucion para la instancia dada.")
