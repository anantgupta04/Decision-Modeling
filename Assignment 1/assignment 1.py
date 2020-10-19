# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 11:09:15 2020

@author: akhilg
"""


import numpy as np
import pandas as pd



# set path where the file has been unzipped
PATH  = ""
assert len(PATH)>0,"Please set the path of the file"
# intializing the relation as an 2-D array
a = np.zeros((6,6))
a = pd.read_csv(PATH+"relations.csv", header=None) 



# to store the dimensions of the relation array
rows, col = a.shape

# to check whether the relation is reflexive
def reflex_check():
    reflex_flag = True
    for i in range(rows):
        for j in range(col):
            if i==j and not a[i][j]:
                reflex_flag = False
                return reflex_flag
    return reflex_flag
        
# to check whether the relation is complete
def complete_check():
    complete_flag = True
    for i in range(rows):
        for j in range(col):
            if not a[i][j] and not a[j][i]:
                complete_flag = False
                return complete_flag
    return complete_flag

# to check whether it is symmetric
def sym_check(mat=[]):
    if len(mat)<=0:
        mat = a
    sym_flag = True
    for i in range(rows):
        for j in range(col):
            if mat[i][j] and mat[i][j] != mat[j][i]:
                sym_flag = False
                return sym_flag
    return sym_flag
 
       
# to check whether the relation is asymmetric or not
def asym_check(mat=[]):
    if len(mat)<=0:
        mat = a
    asym_flag = True
    for i in range(rows):
        for j in range(col):
            if mat[i][j] and mat[i][j] == mat[j][i]:
                asym_flag = False
                return asym_flag
    return asym_flag


# to check whether the relation is anti-symmetric
def anti_sym():
    anti_flag = True
    for i in range(rows):
        for j in range(col):
            if  a[i][j] and a[j][i] and i!=j:
                anti_flag = False
                return anti_flag
    return anti_flag

       
#to check whether the relation is translative
def transitive():
    trans_flag = True
    for i in range(rows):
        for j in range(col):
            if a[i][j] and trans_flag:
                for k in range(rows):
                    if a[j][k] and not a[i][k]:
                        #print("\n\nValue of i = {0}. \n Value of j = {1}, \nValue of k ={2}".format(i,j,k))
                        trans_flag = False
                        return trans_flag
    return trans_flag   


# to check whether the relation is negative translative
def neg_transitive():
    neg_tran = True
    for i in range(rows):
        for j in range(col):
             if not a[i][j] and neg_tran:
                 for k in range(col):
                     if not a[j][k] and a[i][k]:
                         #print("\n\nValue of i = {0}. \n Value of j = {1}, \nValue of k ={2}".format(i,j,k))
                         neg_tran = False
                         return neg_tran
    return neg_tran


# to check whether the relation is complete order
def complete_order():
    if complete_check() and anti_sym() and transitive():
        return True
    else:
        return False
    
    
# to check whether the relation is complete order
def complete_preorder():
    if complete_check() and transitive():
        return True
    else:
        return False

# strict relation
def strict_relation():
    strict_df = np.zeros((rows,col))
    for i in range(rows):
        for j in range(col):
            if a[i][j] and not a[j][i]:
                strict_df[j][i] = 1
    return(strict_df)
    #print("Newly created strict df = \n",strict_df)
 

# Indifference Relation creation
def indifference_relation():
    indiff = np.zeros((rows,col))
    for i in range(rows):
        for j in range(col):
            if a[i][j] and a[j][i]:
                indiff[j][i] = 1
    return(indiff)


    
    
# main function 
if __name__ == '__main__':
    print("\nComplete check for the given relation has a {} result ".format(complete_check()))
    print("\nReflexive check for the given relation has a {} result ".format(reflex_check()))
    print("\nAsymmetric check for the given relation has a {} result ".format(asym_check()))
    print("\nSymmetric check for the given relation has a {} result ".format(sym_check()))
    print("\nAnit-Symmetric check for the given relation has a {} result ".format(anti_sym()))
    print("\nTransitive check for the given relation has a {} result ".format(transitive()))
    print("\nNegative Transitive check for the given relation has a {} result ".format(neg_transitive()))
    print("\nComplete Order check for the given relation has a {} result ".format(complete_order()))
    print("\nComplete Pre-Order check for the given relation has a {} result ".format(complete_preorder()))
    
    df1 = strict_relation()    
    print("\nStrict Relation check for the given relation has a {} result ".format(asym_check(df1)))
    
    df2 = indifference_relation()
    print(df2)
    print("\nIndifferent Relation check for the given relation has a {} result ".format(sym_check(df2)))
    