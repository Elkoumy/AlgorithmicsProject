'''
In this file, we are going to implement the chess ai functions.
Nesma
2/1/2020
'''

from modules.evaluation import *
import time
MaxAllowedTimeInSeconds = 30
inf = float('infinity')

def negamax(curr_position,depth,alpha,beta,player_color,best_move_return,root=True):
    startTime = time.time()
    openings_table = defaultdict(list)
    max_score = -inf 

    if root:
        dict_key = pos_to_key(curr_position)
        if dict_key in openings_table:
            best_move_return[:] = random.choice(openings_table[dict_key]) 
            return

    global lookup  
    lookup = {}

    if depth == 0: 
        final_eval = player_color*evaluate(curr_position) 
        return final_eval 

    possible_moves = all_moves(curr_position, player_color) 

    if not possible_moves: 
        final_eval = player_color*evaluate(curr_position) 
        return final_eval 
    
    if root: 
        best_move = possible_moves[0]

    for move in possible_moves:
        newpos = curr_position.clone() 
        make_move(newpos,move[0][0],move[0][1],int(move[1][0]),int(move[1][1]))
        dict_key = pos_to_key(newpos)  

        if dict_key in lookup:  
            flag = lookup[dict_key]
            print("Exist")
        elif time.time() - startTime > MaxAllowedTimeInSeconds: 
            print("Time Limit of iterative deepining")
            print(depth)
            break
        else:
            flag = -negamax(newpos,depth-1, -beta,-alpha,-player_color,[],False)
            lookup[dict_key] = flag

        if flag > max_score : 
            max_score  = flag
            if root:
                best_move = move
        alpha = max(alpha,flag) 
        if alpha>=beta:
            break

    if root: 
        lookup = {}
        best_move_return[:] = best_move
        return
    return max_score 


#PseudoCode: https://en.wikipedia.org/wiki/Negamax
#Helpful References: https://github.com/Zulko/easyAI/blob/master/easyAI/AI/Negamax.py
#https://github.com/AggressiveBee15/LousyEngine/blob/master/main.py
