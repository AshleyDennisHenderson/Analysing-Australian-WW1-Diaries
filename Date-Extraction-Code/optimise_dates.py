## IMPORT PACKAGES

import string
import math
from math import log
import pandas as pd
from pyomo.environ import *
from pyomo.opt import SolverFactory
from pyomo.opt import SolverStatus, TerminationCondition

def optimise_dates(date_list, I_list, sd, ed, sy, alpha, beta, gamma, delta, omega):

    ## NUMBER OF EXTRACTED DATES

    size = date_list.shape
    n = size[0]

    ## MODEL DECLARATION

    model = ConcreteModel()


    ## INDEX

    model.i = RangeSet(1,n,1)  # Index spanning all extracted dates
    model.j = RangeSet(1,n-1,1)  # Index spanning all extracted dates except the last one


    ## DEFINE VARIABLES

    model.x = Var(model.i, within = NonNegativeIntegers)
    model.d = Var(model.i, within = NonNegativeIntegers, bounds = (1,31))
    model.m = Var(model.i, within = NonNegativeIntegers, bounds = (1,12))
    model.y = Var(model.i, within = NonNegativeIntegers)
    model.D = Var(model.i, within = NonNegativeIntegers)
    model.M = Var(model.i, within = NonNegativeIntegers)
    model.Y = Var(model.i, within = NonNegativeIntegers)
    model.X = Var(model.j, within = NonNegativeIntegers)
    

    ## DEFINE PARAMETERS (KNOWN INFORMATION)

    arr1 = date_list.iloc[:,0].values
    arr1 = arr1.ravel()

    arr2 = date_list.iloc[:,1].values
    arr2 = arr2.ravel()

    arr3 = date_list.iloc[:,2].values
    arr3 = arr3.ravel()

    arr4 = I_list.iloc[:,0].values
    arr4 = arr4.ravel()

    arr5 = I_list.iloc[:,1].values
    arr5 = arr5.ravel()

    arr6 = I_list.iloc[:,2].values
    arr6 = arr6.ravel()

    def par1(model, i):
        return(arr1[i-1])

    def par2(model, i):
        return(arr2[i-1])

    def par3(model, i):
        return(arr3[i-1])

    def par4(model, i):
        return(arr4[i-1])

    def par5(model, i):
        return(arr5[i-1])

    def par6(model, i):
        return(arr6[i-1])

    model.dhat = Param(model.i, initialize = par1)  # Extracted Date
    model.mhat = Param(model.i, initialize = par2)  # Extracted Month
    model.yhat = Param(model.i, initialize = par3)  # Extracted Year

    model.Id = Param(model.i, initialize = par4)  # 
    model.Im = Param(model.i, initialize = par5)  # 
    model.Iy = Param(model.i, initialize = par6)  #
        

    ## DEFINE OBJECTIVE FUNCTION

    def obj_func(model):
        return(alpha*dot_product(model.Id, model.D, index = model.i) + 31*beta*dot_product(model.Im, model.M, index = model.i) + 372*gamma*dot_product(model.Iy, model.Y, index = model.i) + delta*summation(model.X) + omega*model.x[1] - omega*sd)
               
    model.OBJ = Objective(rule = obj_func)

               
    ## DEFINE CONSTRAINTS

    def rule_1(model, i):
        return(sd  - model.x[i] <= 0)
    model.const1 = Constraint(model.i, rule = rule_1)

    def rule_2(model, i):
        return(model.D[i] <= model.k[i]*50)

    def rule_2a(model, j):
        return(model.x[j] -model.x[j+1] <= 0)
    model.const2a = Constraint(model.j, rule = rule_2a)

    def rule_3(model, i):
        return(model.d[i] - model.dhat[i] - model.D[i] <= 0)
    model.const3 = Constraint(model.i, rule = rule_3)

    def rule_4(model, i):
        return(-model.d[i] + model.dhat[i] - model.D[i] <= 0)
    model.const4 = Constraint(model.i, rule = rule_4)

    def rule_5(model, i):
        return(model.m[i] - model.mhat[i] - model.M[i] <= 0)
    model.const5 = Constraint(model.i, rule = rule_5)

    def rule_6(model, i):
        return(-model.m[i] + model.mhat[i] - model.M[i] <= 0)
    model.const6 = Constraint(model.i, rule = rule_6)    

    def rule_7(model, i):
        return(model.y[i] - model.yhat[i] - model.Y[i] <= 0)
    model.const7 = Constraint(model.i, rule = rule_7)

    def rule_8(model, i):
        return(-model.y[i] + model.yhat[i] - model.Y[i] <= 0)
    model.const8 = Constraint(model.i, rule = rule_8)

    def rule_9(model, i):
        return(372*model.y[i] - 372*sy+31*model.m[i] - 31 + model.d[i] - 1 - model.x[i] ==0)
    model.const9 = Constraint(model.i, rule = rule_9)

    def rule_10(model, j):
        return(model.x[j+1]-model.x[j] == model.X[j])
    model.const10 = Constraint(model.j, rule = rule_10)

    def rule_11(model, i):
        return(model.x[i] - ed <= 0)
    model.const11 = Constraint(model.i, rule = rule_11)
               
    ## SOLVE MODEL

    opt = SolverFactory('gurobi')
    opt.options['TimeLimit'] = 300
    results = opt.solve(model)

    if (results.solver.status == SolverStatus.ok) and (results.solver.termination_condition == TerminationCondition.optimal):
        
        opt = 1
        
    elif (results.solver.termination_condition == TerminationCondition.infeasible):
        
        opt = -1
        
    else:
        
       opt = 0
       
    ## CREATE OPTIMISED DATE LIST

    dl = []

    for i in model.i:

        dl.append([model.d[i].value, model.m[i].value, model.y[i].value])

    dl_df = pd.DataFrame(dl)
       



    return(dl_df, opt)
