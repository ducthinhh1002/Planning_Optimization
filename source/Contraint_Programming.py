from ortools.sat.python import cp_model
import os
import time


class ConstraintProgrammingSolver:

    def __init__(self, n_items, n_trucks, items, trucks, time_limit=None):
        self.n_items = n_items
        self.n_trucks = n_trucks
        self.items = items
        self.trucks = trucks

        self.time_limit = time_limit

        self.max_truck_width = max(x[0] for x in trucks)
        self.max_truck_height = max(x[1] for x in trucks)

        self.t_solution = [-1]*self.n_items
        self.x_solution = [-1]*self.n_items
        self.y_solution = [-1]*self.n_items
        self.o_solution = [-1]*self.n_items

    def setModel(self):
        self.model = cp_model.CpModel()

        # T[i, j] means item-i is placed in truck-j
        self.T = {}
        for i in range(self.n_items):
            for j in range(self.n_trucks):
                self.T[i, j] = self.model.NewBoolVar(f'T_{i}_{j}')

        # R[i] means is item-i rotated
        self.R = [self.model.NewBoolVar(f'R_{i}') for i in range(self.n_items)]

        # x[i] is the x-coor of item-i
        self.x = [self.model.NewIntVar(0, self.max_truck_width, f'x_{i}') for i in range(self.n_items)]

        # y[i] is the y-coor of item-i
        self.y = [self.model.NewIntVar(0, self.max_truck_height, f'y_{i}') for i in range(self.n_items)]

        # Z[j] means truck-j is used
        self.Z = [self.model.NewBoolVar(f'Z_{j}') for j in range(self.n_trucks)]

    def setConstraint(self):
        # Each item can only be placed in one truck
        for i in range(self.n_items):
            self.model.Add(sum(self.T[i, j] for j in range(self.n_trucks)) == 1)
            
        # Item cannot be placed out of truck
        for i in range(self.n_items):
            for j in range(self.n_trucks):
                self.model.Add(self.x[i] <= self.trucks[j][0] - self.items[i][0]*(1-self.R[i]) - self.items[i][1]*self.R[i]).OnlyEnforceIf(self.T[i, j])
                self.model.Add(self.y[i] <= self.trucks[j][1] - self.items[i][0]*self.R[i] - self.items[i][1]*(1-self.R[i])).OnlyEnforceIf(self.T[i, j])           

        # Overlap condition
        for i in range(self.n_items-1):
            for k in range(i+1, self.n_items):
                a1 = self.model.NewBoolVar('a1')        
                self.model.Add(self.x[i] + self.items[i][0]*(1-self.R[i]) + self.items[i][1]*self.R[i] <= self.x[k]).OnlyEnforceIf(a1)
                self.model.Add(self.x[i] + self.items[i][0]*(1-self.R[i]) + self.items[i][1]*self.R[i] > self.x[k]).OnlyEnforceIf(a1.Not())
                a2 = self.model.NewBoolVar('a2')        
                self.model.Add(self.y[i] + self.items[i][0]*self.R[i] + self.items[i][1]*(1-self.R[i]) <= self.y[k]).OnlyEnforceIf(a2)
                self.model.Add(self.y[i] + self.items[i][0]*self.R[i] + self.items[i][1]*(1-self.R[i]) > self.y[k]).OnlyEnforceIf(a2.Not())
                a3 = self.model.NewBoolVar('a3')        
                self.model.Add(self.x[k] + self.items[k][0]*(1-self.R[k]) + self.items[k][1]*self.R[k] <= self.x[i]).OnlyEnforceIf(a3)
                self.model.Add(self.x[k] + self.items[k][0]*(1-self.R[k]) + self.items[k][1]*self.R[k] > self.x[i]).OnlyEnforceIf(a3.Not())
                a4 = self.model.NewBoolVar('a4')        
                self.model.Add(self.y[k] + self.items[k][0]*self.R[k] + self.items[k][1]*(1-self.R[k]) <= self.y[i]).OnlyEnforceIf(a4)
                self.model.Add(self.y[k] + self.items[k][0]*self.R[k] + self.items[k][1]*(1-self.R[k]) > self.y[i]).OnlyEnforceIf(a4.Not())

                for j in range(self.n_trucks):
                    self.model.AddBoolOr(a1, a2, a3, a4).OnlyEnforceIf(self.T[i, j], self.T[k, j])
    
        # Find which truck has been used 
        for k in range(self.n_trucks):
            self.model.Add(self.Z[k] <= sum(self.T[i,k] for i in range(self.n_items)))
            self.model.Add(sum(self.T[i,k] for i in range(self.n_items)) <= self.Z[k] * self.n_items)

    def setObjective(self):
        # Objective function: Minimize the total cost of the trucks used
        self.cost = sum(self.Z[j] * self.trucks[j][2] for j in range(self.n_trucks))
        self.model.Minimize(self.cost)

    def solve(self):

        self.setModel()
        self.setConstraint()
        self.setObjective()

        solver = cp_model.CpSolver()
        
        if self.time_limit is not None:
            solver.parameters.max_time_in_seconds = self.time_limit

        # Start the timer
        start_time = time.time()
        status = solver.Solve(self.model)

        # End the timer
        end_time = time.time()
        self.solve_time = end_time - start_time

        if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
            for i in range(self.n_items):
                for j in range(self.n_trucks):
                    if solver.Value(self.T[i, j]) == 1:
                        self.t_solution[i] = j

                self.x_solution[i] = solver.Value(self.x[i])
                self.y_solution[i] = solver.Value(self.y[i])
                self.o_solution[i] = 1 if solver.Value(self.R[i]) == 1 else 0
            
            # Get the total cost
            self.total_cost = solver.ObjectiveValue()

    def printSolution(self):
        for i in range(self.n_items):
            print(i+1, self.t_solution[i]+1, self.x_solution[i], self.y_solution[i], self.o_solution[i])
        
        # Print total cost and solve time
        # print(f'Total cost: {self.total_cost}')
        # print(f'Solve time: {self.solve_time} seconds')

if __name__ == "__main__":
    n_items, n_trucks = map(int, input().split())
    items = [tuple(map(int, input().split())) for i in range(n_items)]
    trucks = [tuple(map(int, input().split())) for i in range(n_trucks)]   
    solver = ConstraintProgrammingSolver(n_items, n_trucks, items, trucks)
    solver.solve()
    solver.printSolution()
