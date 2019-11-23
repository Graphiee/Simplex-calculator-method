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
            np.put(zeros, artificial*rows+columns, np.ones(artificial))
            zeros = zeros.reshape((len(lhs), artificial))
            lhs = np.concatenate((lhs, zeros), axis=1)

        for iteration in range(num_iter):
            print(iteration)
            #z_j - obj
            base_indexes = np.where((np.sum(lhs, axis=0) == 1) & (np.sum(lhs == 0, axis=0) == len(lhs)-1))[0]
            base_values = obj[base_indexes]
            z_j = np.dot(base_values.reshape(1,-1), lhs)
            obj_zj = z_j - obj
            obj_zj = obj_zj.flatten()


            #Pivot element
            if self.maximalize:
                if any(obj_zj < 0):
                    obj_zj_index = int(np.where(obj_zj == min(obj_zj))[0])
                    vector_ratio = rhs/lhs[:, obj_zj_index][0]
                else:
                    print('Optimal solution reached after {} iterations.'.format(iteration))
            elif not self.maximalize:
                if any(obj_zj > 0):
                    obj_zj_index = int(np.where(obj_zj == max(obj_zj))[0])
                    vector_ratio = rhs/lhs[:, obj_zj_index][0]
                else:
                    print('Optimal solution reached after {} iterations.'.format(iteration))

            min_ratio_index = int(np.where(vector_ratio == min(vector_ratio))[0])
            pivot = lhs[min_ratio_index, obj_zj_index]

            new_row = lhs[min_ratio_index] / pivot
            lhs = lhs - lhs[:, obj_zj_index].reshape(-1,1) * new_row
            lhs[min_ratio_index,:] = new_row
        return lhs



first = Simplex(objective = [30, 20],
                lhs = [[2, 1],
                       [3, 3],
                       [1.5, 0]],
                rhs = [1000,2400,600] ,
                inequality_dir = ['<=', '<=', '<='],
                maximalize=True)

print(first.fit(num_iter=2))