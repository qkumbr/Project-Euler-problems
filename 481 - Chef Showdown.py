#10/24/14 - m.v.

from __future__ import division
from decimal import Decimal
import copy

probability_matrix = []
showdowns = [0]

def increase_showdowns():
    showdowns[0] += 1

def get_showdowns():
    return showdowns[0]

def fib(n):
    if n == 1 or n == 2:
        return 1
    else:
        return fib(n - 1) + fib(n - 2)

def build_probability_matrix(numchefs):
    #print "building probability matrix..."
    for i in range (1, numchefs + 1):
        probability_matrix.append([i, 0])
    #print "probability matrix is ", get_probability_matrix()

def set_probability_matrix(winner, increase):
    var = '%.8f' % round(increase,8)
    newvar = Decimal(var)
    for i in probability_matrix:
        if i[0] == winner:
            i[1] += newvar

def get_probability_matrix():
    return probability_matrix

def build_chef_list(probabilities):
    chefs_list = []
    for i in range(0, len(probabilities)):
        chefs_list.append([i + 1, probabilities[i], 0, 0])
    build_probability_matrix(len(probabilities))
    return chefs_list

def remaining_chefs(chefs):
    num_remaining = 0
    for i in chefs:
        if i[3] == 0:
            num_remaining += 1
    return num_remaining

def probability_of_all_remaining_chefs_losing(chefs):
    prob = 1
    for i in chefs:
        if i[3] == 0:
            prob *= 1-i[1]
    return prob    

def eliminate(c):
    chefs = copy.deepcopy(c) #have to do this because python passes objects by memory address. this is to keep anything in the list from changing outside this function
    max_remaining_probability = 0    
    #print "elimination function called"
    for i in range (1, (len(chefs))):
        #print "evaluating chef: ", chefs[i]
        if chefs[i][3] == 0:
            max_remaining_probability = max(max_remaining_probability, chefs[i][1])
    #print "max prob of all chefs: ", max_remaining_probability
    for j in range (1, (len(chefs))):
        #print "evaluating chef: ", chefs[j], " for elimination"
        if chefs[j][1] == max_remaining_probability:
            #print "chef ", chefs[j], "has max probability of winning."
            #print "further evaluating chef: ", chefs[j]        
            if chefs[j][3] == 0:
                chefs[j][3] = 1
                #print "chef ", chefs[j], " eliminated"
                break
    return chefs     

def win(c, accumulated_probability, r, p):
    increase_showdowns()
    remaining_chefs = copy.deepcopy(r)
    prob_of_all_losses = copy.deepcopy(p)
    #print "prob of all losses ", prob_of_all_losses
    #print "accumulated probability is ", accumulated_probability
    chefs = copy.deepcopy(c)
    index_of_chef_to_eliminate = 0
    #print "win function called. eliminating chefs"
    ###chefs = eliminate(chefs)   

    max_remaining_probability = 0    
    #print "elimination function called"
    for i in range (1, (len(chefs))):
        #print "evaluating chef: ", chefs[i]
        if chefs[i][3] == 0:
            if max_remaining_probability < chefs[i][1]:
                max_remaining_probability = chefs[i][1]
                index_of_chef_to_eliminate = i
    #print "max prob of all chefs: ", max_remaining_probability
    chefs[index_of_chef_to_eliminate][3] = 1
    if chefs[index_of_chef_to_eliminate][1] < 1: #avoiding a divide-by-zero error here
        prob_of_all_losses = prob_of_all_losses / (1 - chefs[index_of_chef_to_eliminate][1])
    else:
        prob_of_all_losses = probability_of_all_remaining_chefs_losing(chefs)
    remaining_chefs -= 1

    #print "results of elimination: ", chefs
    #print "remaining chefs ", remaining_chefs
    #print "prob of all losses ", prob_of_all_losses
    ###if remaining_chefs(chefs) == 1:
    if remaining_chefs == 1:
        #do not do another match
        #print "only one chef remains."
        #print "winner: ", chefs[0]
        #print "applying win results in win function"
        #print "adding accumulated probability", accumulated_probability
        set_probability_matrix(chefs[0][0], accumulated_probability)
        #print "probability matrix is now", get_probability_matrix()
        #print "prior to returning win results, chefs just for this function are ", chefs
        #print "win function exiting..."
    else: #competitors do exist
        #print "more than one competitor exists. moving on within win function: ", chefs
        #move the winner to the back of the list
        chefs.append(chefs.pop(0)) #move the winner to the back
        while chefs[0][3] == 1: #move ineligible chefs to the back
            chefs.append(chefs.pop(0))
        #call showdown with the next competitor
        #print "ending win function and calling next showdown with chefs: ", chefs
        showdown(chefs, accumulated_probability, 0, remaining_chefs, prob_of_all_losses)
    return chefs

def lose(c, accumulated_probability, num_losses, r, p):
    increase_showdowns()
    remaining_chefs = copy.deepcopy(r)
    prob_of_all_losses = copy.deepcopy(p)
    #print "prob of all losses ", prob_of_all_losses
    #print "start of lose function with num_losses = ", num_losses
    chefs = copy.deepcopy(c)
    #if num_losses < (remaining_chefs(chefs)): otherwise do nothing because you're in an infinite loop
    if num_losses < remaining_chefs: #otherwise do nothing because you're in an infinite loop
        #print "loss function is rotating chefs to the next eligible chef."
        #print "prior to rotation, chefs are: ", chefs
        chefs.append(chefs.pop(0)) #move the loser to the back
        while chefs[0][3] == 1: #move ineligible chefs to the back
            chefs.append(chefs.pop(0))
        #print "rotation complete. lose function is now calling showdown function..."
        #print "...with chefs ", chefs
        showdown(chefs, accumulated_probability, num_losses, remaining_chefs, prob_of_all_losses)
        #print "lose function is returning chefs: ", chefs
    return chefs

def showdown(chefs, accumulated_probability, num_losses, r, p):
    increase_showdowns()
    what_you_started_with = copy.deepcopy(chefs)
    prob_of_all_losses = copy.deepcopy(p)
    #print "prob of all losses ", prob_of_all_losses
    remaining_chefs = copy.deepcopy(r)
    print "start of showdown function"
    print "chefs before calling win function are: ", chefs
    if chefs[0][1] > 0: #chef can't win if their probability is 0
        newchefs = []
        #newchefs = win(chefs, ((accumulated_probability * chefs[0][1]) / (1 - probability_of_all_remaining_chefs_losing(chefs))))
        newchefs = win(chefs, ((accumulated_probability * chefs[0][1]) / (1 - prob_of_all_losses)), remaining_chefs, prob_of_all_losses)
        #chefs = copy.deepcopy(newchefs)
        #print "chefs after calling win function are: ", chefs
    chefs = what_you_started_with
    if chefs[0][1] < 1: # chef can't lose if their probability is 1
        newchefs = []
        #print "calling lose function with: ", chefs
        newchefs = lose(chefs, accumulated_probability * (1 - chefs[0][1]), num_losses + 1, remaining_chefs, prob_of_all_losses)
        chefs = copy.deepcopy(newchefs)
    chefs = what_you_started_with
    print "end of showdown. returning chefs: ", chefs
    return chefs

numchefs = input("number of chefs? ")
probabilities = []
for i in range(1, numchefs + 1):
    var = fib(i)/fib(numchefs + 1)
    var = '%.8f' % round(var,8)
    newvar = Decimal(var)
    probabilities.append(newvar)
print "probabilities after doing fib shit are: ", probabilities
chefs = build_chef_list(probabilities)
print "entering showdown with chefs: ", chefs
print "BATTLE START"
chefs = showdown(chefs, 1, 0, numchefs, probability_of_all_remaining_chefs_losing(chefs))
print "game over!", 
print "we started with chefs: ", chefs
print "final results are: "
for i in get_probability_matrix():
    print "chef",i[0],":", i[1]
print "there were", get_showdowns(), "nodes"
print "every puzzle has a solution"
print "bye bye"
