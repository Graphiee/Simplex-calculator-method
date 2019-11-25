import numpy as np

class Simplex:

    def __init__(self, objective, lhs, rhs, inequality_dir ,maximalize=True):
        self.objective = objective
        self.lhs = lhs
        self.inequality_dir = inequality_dir
        self.rhs = rhs
        self.maximalize = maximalize

    def fit(self, num_iter=100):

        obj = np.array(self.objective.copy())
        lhs = np.array(self.lhs.copy())
        rhs = np.array(self.rhs.copy())
        inequalities = np.array(self.inequality_dir)
        if any(rhs < 0):
            less_than_0 = np.where(rhs<0)[0]
            rhs[less_than_0] = -rhs[less_than_0]
            lhs[less_than_0] = -lhs[less_than_0]
            inequalities[less_than_0] = np.where(inequalities[less_than_0] == '<=', '>=',
                                                 np.where(inequalities[less_than_0] == '>=','<=','='))

        slacks = sum((inequalities == '>=') | (inequalities == '<='))
        artificial = sum((inequalities == '=') | (inequalities == '>='))

        obj = np.append(obj, [0 for i in range(slacks)])
        obj = np.append(obj, [-1e64 if self.maximalize==True else 1e64 for i in range(artificial)])
        #Slacks
        if slacks > 0 :
            zeros = np.zeros((len(lhs) * slacks))
            rows = np.where((inequalities == '>=') | (inequalities == '<='))[0]
            columns = np.array(range(slacks))
            np.put(zeros, slacks * rows + columns, np.ones(slacks))
            zeros = np.where(np.tile(inequalities, slacks) == '>=', -zeros, zeros)
            zeros = zeros.reshape((len(lhs), slacks))
            lhs = np.concatenate((lhs, zeros), axis=1)

        #Artificials
        if artificial > 0:
            zeros = np.zeros((len(lhs) * artificial))
            rows = np.where((inequalities == '>=') | (inequalities == '='))[0]
            columns = np.array(range(artificial))
            np.put(zeros, artificial * rows + columns, np.ones(artificial))
            zeros = zeros.reshape((len(lhs), artificial))
            lhs = np.concatenate((lhs, zeros), axis=1)
        for iteration in range(num_iter):

            #z_j - obj
            base_indexes = np.where((np.sum(lhs, axis=0) == 1) & (np.sum(lhs == 0, axis=0) == len(lhs)-1))[0]
            base_indexes = base_indexes[-len(lhs):]
            print(base_indexes)
            base_values = obj[base_indexes]
            base_table = lhs[:,base_indexes]
            base_table_correct = np.eye(len(lhs))
            correction = np.nonzero(base_table_correct)[1]- (np.nonzero(base_table_correct)[1] - np.nonzero(base_table)[1])
            base_values = base_values[correction]
            z_j = np.dot(base_values.reshape(1,-1), lhs)
            obj_zj = z_j - obj
            obj_zj = obj_zj.flatten()
            function_score = np.dot(base_values, rhs)
            #Pivot element
            if self.maximalize:
                if any(obj_zj < 0):
                    index = np.where(obj_zj == min(obj_zj))[0]
                    if len(index) > 1:
                        obj_zj_index = int(index[0])
                    else:
                        obj_zj_index = int(index)
                    np.seterr(divide='ignore',invalid='ignore')
                    vector_ratio = rhs/lhs[:, obj_zj_index]
                    vector_ratio[np.where(vector_ratio < 0)] = np.Inf
                else:
                    print('Optimal solution reached after {} iterations.'.format(iteration+1))
                    break
            elif not self.maximalize:
                if any(obj_zj > 0):
                    obj_zj_index = int(np.where(obj_zj == max(obj_zj))[0])
                    np.seterr(divide='ignore', invalid='ignore')
                    vector_ratio = rhs/lhs[:, obj_zj_index]
                    if vector_ratio < 0:
                        vector_ratio[np.where(vector_ratio<0)] = np.Inf
                else:
                    print('Optimal solution reached after {} iterations.'.format(iteration+1))
                    break

            if all((vector_ratio < 0) | (vector_ratio == np.Inf)):
                raise RuntimeError('A linear program is infeasible.')
            min_ratio_index = int(np.where(vector_ratio == min(vector_ratio))[0])
            pivot = lhs[min_ratio_index, obj_zj_index]
            base_table_correct[:, min_ratio_index] = lhs[:, obj_zj_index]
            rhs = np.dot(np.linalg.inv(base_table_correct), rhs)
            new_row = lhs[min_ratio_index] / pivot
            lhs = lhs - lhs[:, obj_zj_index].reshape(-1,1) * new_row
            lhs[min_ratio_index,:] = new_row
            print(base_indexes)


        # return function_score, rhs

first = Simplex(objective = [1, -1, 2],
                lhs = [[2,2,0],[0,0,1]],
                rhs = [8,5],
                inequality_dir = ['<=','<='],
                maximalize=True)

print(first.fit(num_iter=10))