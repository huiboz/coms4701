"""
COMS W4701 Artificial Intelligence - Programming Homework 1

In this assignment you will implement and compare different search strategies
for solving the n-Puzzle, which is a generalization of the 8 and 15 puzzle to
squares of arbitrary size (we will only test it with 8-puzzles for now).
See Courseworks for detailed instructions.

@author: Huibo Zhao (hz2480)
"""

import time

def state_to_string(state):
    row_strings = [" ".join([str(cell) for cell in row]) for row in state]
    return "\n".join(row_strings)


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

# recover the solution
def recover(parents,actions,state):
    result = []
    current_state = state

    while current_state in parents:
        result.insert(0,actions[current_state])
        current_state = parents[current_state]

    return result

def bfs(state):
    """
    Breadth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.
    """
    parents = {}
    actions = {}

    states_expanded = 0
    max_frontier = 0

    #YOUR CODE HERE

    #Hint: You may start with this:
    frontier = [state]
    explored = set()
    seen = set()
    seen.add(state)

    while frontier:
        max_frontier = max(max_frontier,len(frontier))
        leaf_node = frontier.pop(0)
        explored.add(leaf_node)

        if goal_test(leaf_node) is True:
            states_expanded = len(explored)
            action_recovers = recover(parents,actions,leaf_node)
            return action_recovers, states_expanded, max_frontier


        successors = get_successors(leaf_node)
        for i in range(len(successors)):
            current_state = successors[i][1]
            if current_state not in explored and current_state not in seen:
                frontier.append(current_state)
                seen.add(current_state)
                parents[current_state] = leaf_node
                actions[current_state] = successors[i][0]


    #  return solution, states_expanded, max_frontier
    return None, states_expanded, max_frontier # No solution found


def dfs(state):
    """
    Depth first search.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.
    """

    parents = {}
    actions = {}

    states_expanded = 0
    max_frontier = 0

    #YOUR CODE HERE

    frontier = [state]
    explored = set()
    seen = set()
    seen.add(state)

    while frontier:
        max_frontier = max(max_frontier,len(frontier))
        leaf_node = frontier.pop()
        explored.add(leaf_node)

        if goal_test(leaf_node) is True:
            states_expanded = len(explored)
            action_recovers = recover(parents,actions,leaf_node)
            return action_recovers, states_expanded, max_frontier


        successors = get_successors(leaf_node)
        for i in range(len(successors)):
            current_state = successors[i][1]
            if current_state not in explored and current_state not in seen:
                frontier.append(current_state)
                seen.add(current_state)
                parents[current_state] = leaf_node
                actions[current_state] = successors[i][0]


    #  return solution, states_expanded, max_frontier

    return None, states_expanded, max_frontier # No solution found


def misplaced_heuristic(state):
    """
    Returns the number of misplaced tiles.
    """

    #YOUR CODE HERE
    misplace = 0
    for i in range(0,3):
        for j in range(0,3):
            expected_num = i * 3 + j
            if (state[i][j] != expected_num):
                misplace+=1

    return misplace


def manhattan_heuristic(state):
    """
    For each misplaced tile, compute the manhattan distance between the current
    position and the goal position. THen sum all distances.
    """
    cost = 0

    for num in range(1,9):
        for i in range(0,3):
            for j in range(0,3):
                if (state[i][j] == num):
                    original_row = num//3
                    original_column = num%3
                    cost += abs(i-original_row)
                    cost += abs(j-original_column)

    return cost


def best_first(state, heuristic = misplaced_heuristic):
    """
    Breadth first search using the heuristic function passed as a parameter.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.
    """

    # You might want to use these functions to maintain a priority queue
    from heapq import heappush
    from heapq import heappop

    parents = {}
    actions = {}
    costs = {}
    costs[state] = 0

    states_expanded = 0
    max_frontier = 0

    #YOUR CODE HERE


    frontier = [(costs[state],state)]
    explored = set()
    seen = set()
    seen.add(state)

    while frontier:
        max_frontier = max(max_frontier,len(frontier))
        leaf_node = (heappop(frontier))[1]
        explored.add(leaf_node)

        if goal_test(leaf_node) is True:
            states_expanded = len(explored)
            action_recovers = recover(parents,actions,leaf_node)
            return action_recovers, states_expanded, max_frontier

        successors = get_successors(leaf_node)
        for i in range(len(successors)):
            current_state = successors[i][1]
            if current_state not in seen:
                costs[current_state] = heuristic(current_state)
                heappush(frontier,(costs[current_state],current_state))
                seen.add(current_state)
                parents[current_state] = leaf_node
                actions[current_state] = successors[i][0]

    return None, states_expanded, max_frontier


def astar(state, heuristic = misplaced_heuristic):
    """
    A-star search using the heuristic function passed as a parameter.
    Returns three values: A list of actions, the number of states expanded, and
    the maximum size of the frontier.
    """
    # You might want to use these functions to maintain a priority queue

    from heapq import heappush
    from heapq import heappop

    parents = {}
    actions = {}
    costs = {}
    costs[state] = 0

    states_expanded = 0
    max_frontier = 0

    #YOUR CODE HERE


    frontier = [(costs[state],state)]
    explored = set()
    seen = set()
    seen.add(state)

    while frontier:
        max_frontier = max(max_frontier,len(frontier))
        leaf_node = (heappop(frontier))[1]
        explored.add(leaf_node)

        if goal_test(leaf_node) is True:
            states_expanded = len(explored)
            action_recovers = recover(parents,actions,leaf_node)
            return action_recovers, states_expanded, max_frontier

        successors = get_successors(leaf_node)
        for i in range(len(successors)):
            current_state = successors[i][1]
            if current_state not in explored:
                hcost = heuristic(current_state)
                ccost = 1 + costs[leaf_node] - heuristic(leaf_node)
                total_cost = hcost + ccost

                if current_state not in seen:
                    costs[current_state] = total_cost
                    heappush(frontier,(costs[current_state],current_state))
                    seen.add(current_state)
                    parents[current_state] = leaf_node
                    actions[current_state] = successors[i][0]
                else:
                    if total_cost < costs[current_state]:  # update!
                        frontier.remove((costs[current_state],current_state))
                        heappush(frontier,(total_cost,current_state))
                        costs[current_state] = total_cost
                        parents[current_state] = leaf_node
                        actions[current_state] = successors[i][0]

    return None, states_expanded, max_frontier # No solution found


def print_result(solution, states_expanded, max_frontier):
    """
    Helper function to format test output.
    """
    if solution is None:
        print("No solution found.")
    else:
        print("Solution has {} actions.".format(len(solution)))
    print("Total states expanded: {}.".format(states_expanded))
    print("Max frontier size: {}.".format(max_frontier))



if __name__ == "__main__":

    #Easy test case
    
    test_state = ((1, 4, 2),
                  (0, 5, 8),
                  (3, 6, 7))

    '''
    #More difficult test case
    test_state = ((7, 2, 4),
                  (5, 0, 6),
                  (8, 3, 1))
    '''



    print(state_to_string(test_state))
    print()


    print("====BFS====")
    start = time.time()
    solution, states_expanded, max_frontier = bfs(test_state) #
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    if solution is not None:
        print(solution)
    print("Total time: {0:.3f}s".format(end-start))



    print()
    print("====DFS====")
    start = time.time()
    solution, states_expanded, max_frontier = dfs(test_state)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    print("Total time: {0:.3f}s".format(end-start))


    print()
    print("====Greedy Best-First (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_frontier = best_first(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Misplaced Tiles Heuristic)====")
    start = time.time()
    solution, states_expanded, max_frontier = astar(test_state, misplaced_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    print("Total time: {0:.3f}s".format(end-start))

    print()
    print("====A* (Total Manhattan Distance Heuristic)====")
    start = time.time()
    solution, states_expanded, max_frontier = astar(test_state, manhattan_heuristic)
    end = time.time()
    print_result(solution, states_expanded, max_frontier)
    print("Total time: {0:.3f}s".format(end-start))
