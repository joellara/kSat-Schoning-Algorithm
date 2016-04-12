import random
import string
import Schoning
def generate(num_clauses = 20,num_sat=3):
    instance = []
    union_str = ")a("

    for _ in range(0,num_clauses):
        clause = ""
        lts = string.ascii_uppercase
        for s in range(0,num_sat):
            not_str = ""
            if random.choice([True,False]):
                not_str = "n"
            letter = random.choice(lts)
            lts = lts.replace(letter,"")
            clause += not_str+letter
            if s < num_sat-1:
                clause+="o"
        instance.append(clause)
    union_str = union_str.join([str(x) for x in instance])
    return "("+union_str+")"
if __name__ == "__main__":
    rand_clause = generate(12,2)
    print(rand_clause)
    print(Schoning.schoning_algo(rand_clause))