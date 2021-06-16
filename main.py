import numpy as np

#first iteration using the technique of sorthing everything as close to the left as possible and as close to the right as possible
def get_probabilities_simple(board_size, hints):
    left_result=np.array([0]*board_size)
    right_result=np.array([0]*board_size)

    #create left stacked results
    left_ptr=0
    index=1
    for i in hints:
        left_result[left_ptr:left_ptr+i]=[index]*i
        left_ptr=left_ptr+i+1
        index=index+1

    #create right stacked results
    right_ptr=board_size
    index=len(hints)
    for i in np.flip(hints):
        right_result[right_ptr-i:right_ptr]=[index]*i
        right_ptr=right_ptr-(i+1)
        index=index-1

    #compare for final results
    result=np.array([0]*board_size)
    for i in range(board_size):
        if (left_result[i] != 0 and left_result[i]==right_result[i]):
            result[i]=1
    return result

# second iteration to brute force all possible combinations (probably recursively) NOT WORKING
#def get_probabilities_brute(board_size, hints):

print(get_probabilities_simple(20, np.array([1,3,9])))
print(get_probabilities_simple(20, np.array([5,5,5])))