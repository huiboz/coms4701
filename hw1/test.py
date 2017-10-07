from heapq import heappush, heappop


def swap_cells(state, i1, j1, i2, j2):
    """
    Returns a new state with the cells (i1,j1) and (i2,j2) swapped.
    """
    value1 = state[i1][j1]
    value2 = state[i2][j2]

    new_state = []
    for row in range(len(state)):
        new_row = []
        for column in range(len(state[row])):
            if row == i1 and column == j1:
                new_row.append(value2)
            elif row == i2 and column == j2:
                new_row.append(value1)
            else:
                new_row.append(state[row][column])
        new_state.append(tuple(new_row))
    return tuple(new_state)

def get_successors(state):
    """
    This function returns a list of possible successor states resulting
    from applicable actions.
    The result should be a list containing (Action, state) tuples.
    For example [("Up", ((1, 4, 2),(0, 5, 8),(3, 6, 7))),
                 ("Left",((4, 0, 2),(1, 5, 8),(3, 6, 7)))]
    """

    child_states = []

    # YOUR CODE HERE . Hint: Find the "hole" first, then generate each possible
    # successor state by calling the swap_cells method.
    # Exclude actions that are not applicable.
    row = 0
    column = 0

    for i in range(0,3):
        for j in range(0,3):
            if (state[i][j] == 0):
                row = i;
                column = j;


    if (column<2):
        child_states.append(("Left",swap_cells(state,row,column,row,column+1)))
    if (column>0):
        child_states.append(("Right",swap_cells(state,row,column,row,column-1)))
    if (row<2):
        child_states.append(("Up",swap_cells(state,row,column,row+1,column)))
    if (row>0):
        child_states.append(("Down",swap_cells(state,row,column,row-1,column)))

    return child_states


def goal_test(state):
    """
    Returns True if the state is a goal state, False otherwise.
    """

    #YOUR CODE HERE
    if (state != ((0,1,2),(3,4,5),(6,7,8))):
        return False
    else:
        return True

def recover(parents,actions,state):
    result = []
    current_state = state

    while current_state in parents:
        result.insert(0,actions[current_state])
        current_state = parents[current_state]

    return result





state = ((1,3,5),(2,4,6),(8,0,7))
state2 = ((0,1,2),(3,4,5),(6,7,8))

cost = 0

for num in range(0,9):
    for i in range(0,3):
        for j in range(0,3):
            if (state[i][j] == num):
                original_row = num//3
                original_column = num%3
                cost += abs(i-original_row)
                cost += abs(j-original_column)

print (cost)


for num2 in range(1,9):
    print(num2)
