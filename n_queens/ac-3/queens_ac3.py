class CSP:
    def __init__(self, variables, domains, constraints, neighbors):
        self.variables = variables
        self.domains = domains
        self.constraints = constraints
        self.neighbors = neighbors


def initialize_csp(n):
    variables = [i for i in range(n)]
    domains = {i: [j for j in range(n)] for i in range(n)}
    neighbors = {i: [] for i in range(n)}
    for i in range(n):
        for j in range(i + 1, n):
            neighbors[i].append(j)
            neighbors[j].append(i)
    return CSP(variables, domains, n_queens_constraint, neighbors)


def n_queens_constraint(X_i, x, X_j, y):
    return x != y and abs(x - y) != abs(X_i - X_j)


def revise(csp, X_i, X_j):
    revised = False
    for x in csp.domains[X_i][:]:
        if not any(csp.constraints(X_i, x, X_j, y) for y in csp.domains[X_j]):
            csp.domains[X_i].remove(x)
            revised = True
    return revised


def AC3(csp):
    queue = [(X_i, X_j) for X_i in csp.variables for X_j in csp.neighbors[X_i]]
    while queue:
        (X_i, X_j) = queue.pop(0)
        if revise(csp, X_i, X_j):
            if len(csp.domains[X_i]) == 0:
                return False
            for X_k in csp.neighbors[X_i]:
                if X_k != X_j:
                    queue.append((X_k, X_i))
    return True


def n_queens_AC3(n):
    csp = initialize_csp(n)
    if AC3(csp):
        return csp  # Returns a solution
    else:
        return "No solution exists"

# Helper function to print the solution


def print_solution(csp):
    solution = [-1] * len(csp.variables)
    for var in csp.variables:
        solution[var] = csp.domains[var][0]
    print("N-Queens solution:", solution)


# Example usage
n = 8  # Size of the chessboard
result = n_queens_AC3(n)
if result != "No solution exists":
    print_solution(result)
else:
    print(result)
