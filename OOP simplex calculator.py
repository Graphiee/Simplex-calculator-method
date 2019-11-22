import numpy as np

class Simplex:

    def __init__(self, objective, constraints, inequality_dir ,maximalize=True):
        self.objective = objective
        self.constraints = constraints
        self.maximalize = maximalize
        self.inequality_dir = inequality_dir

    def fit(self, num_iter=100):

        obj = np.array(self.objective.copy())
        con = np.array(self.constraints.copy())
        inequalities = np.array(self.inequality_dir)
        slacks = sum((inequalities == '>=') | (inequalities == '<='))
        artificial = sum((inequalities == '=') | (inequalities == '>='))

        obj = np.append(obj, [0 for i in range(slacks)])
        obj = np.append(obj, [-1e64 for i in range(artificial)])

        constraints_m = {}
        for i in range(num_iter):
            for constraint in range(len(con)):
                if len(con) == to_append_slack:
                    break
                to_append_slack = np.zeros(slacks)
                to_append_art = np.zeros(artificial)
                if inequalities[constraint] == '<=':
                    to_append_slack[constraint] = 1
                    constraints_m['Constraint_' + str(constraint)] = np.append(con[constraint], to_append_slack)
                elif inequalities[constraint] == '>=':
                    to_append_slack[constraint] = -1
                    constraints_m['Constraint_' + str(constraint)] = np.append(con[constraint], to_append_slack)

            # for constraint in range(len(con)):
            #     if inequalities[constraint] == '=':
            #         constraints_m['Constraint_' + str(constraint)] = np.append(con[constraint], to_append_slack)


first = Simplex(objective = [30, 20],
                constraints = [[2, 1, 1000],
                               [3, 3, 2400],
                               [1.5, 600]],
                inequality_dir = ['>=', '=', '>='])
