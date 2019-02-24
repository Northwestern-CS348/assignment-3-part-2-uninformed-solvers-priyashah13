
from solver import *


class SolverDFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Depth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """
        # Student code goes here

        curr = self.currentState
        # check the base case
        # if the victory condition is met, just return True, and done.
        if curr.state == self.victoryCondition:
            return True
        # however, if the victory condition is not met, go through the DFS
        else:
            # get all movables that are possible form the current statement
            movables = self.gm.getMovables()
            # print(self.currentState.depth, movables)
            if not curr.children and movables:
                # when there are no more children and there are movables,
                # for every possible, explore that move by making the move, saving the game state as a child
                # then reverse the move
                for move in movables:
                    self.gm.makeMove(move)
                    # increase depth by one because we are at the next depth
                    d = curr.depth+1
                    next = GameState(self.gm.getGameState(), d, move)
                    # print(next.state)
                    curr.children.append(next)
                    next.parent = curr
                    self.gm.reverseMove(move)
        while len(curr.children) > curr.nextChildToVisit:
            # do the following while there are still children left to visit
            # go to the next child in the list of children
            next = curr.children[curr.nextChildToVisit]
            # increment the index
            curr.nextChildToVisit += 1
            # if the child was not previously visited,
            # walk the child using DFS
            if next not in self.visited:
                self.walk(next)
                if self.currentState.state == self.victoryCondition:
                    return True
                break
            self.unwalk()
        return False

    def walk(self, next):
        # first mark the child as visited
        self.visited[next] = True
        # make the move that got us to the next
        # then update the current state with the child's state
        self.gm.makeMove(next.requiredMovable)
        self.currentState = next

    def unwalk(self):
        # while self.currentState exists and all the children have been visited
        while self.currentState and self.currentState.nextChildToVisit == len(self.currentState.children):
            # keep going up the tree
            self.gm.reverseMove(self.currentState.requiredMovable)
            # set the parent as the current state so we can keep moving up
            self.currentState = self.currentState.parent


class SolverBFS(UninformedSolver):
    def __init__(self, gameMaster, victoryCondition):
        super().__init__(gameMaster, victoryCondition)

    def solveOneStep(self):
        """
        Go to the next state that has not been explored. If a
        game state leads to more than one unexplored game states,
        explore in the order implied by the GameMaster.getMovables()
        function.
        If all game states reachable from a parent state has been explored,
        the next explored state should conform to the specifications of
        the Breadth-First Search algorithm.

        Returns:
            True if the desired solution state is reached, False otherwise
        """

        curr = self.currentState
        # initial check for victory state
        if curr.state == self.victoryCondition:
            return True
        # mark the currentState as visited
        self.visited[curr] = True

        # get all movables that are possible form the current statement
        # same logic as DFS
        movables = self.gm.getMovables()
        # print(self.currentState.depth, movables)
        if movables and not curr.children:
            # same logic as DFS, for each move, store the game state as the children for the current state
            for move in movables:
                self.gm.makeMove(move)
                newState = GameState(self.gm.getGameState(), curr.depth + 1, move)
                newState.parent = curr
                curr.children.append(newState)
                # reverse the move
                self.gm.reverseMove(move)
        # go through the entire tree
        self.search()
        return False

    def search(self):
        # while a parent exists, and the currentState is the last sibling,
        # go up the tree
        while self.currentState.parent and len(self.currentState.parent.children)-1 == self.getIndex(self.currentState):
            # reverse the move that was used to get to currentState
            self.gm.reverseMove(self.currentState.requiredMovable)
            # and update the current state to be the parent
            self.currentState = self.currentState.parent
        # we get out of the while loop when the child is not the last of the siblings
        # we hit this case when a parent exists
        # therefore, we want to move to the next sibling
        if self.currentState.parent:
            # must go up the tree one step,
            # then we update the index to be one more than that of the current state
            self.gm.reverseMove(self.currentState.requiredMovable)
            next_index = self.getIndex(self.currentState)+1
            # set the current state to be the next sibling using the new index
            self.currentState = self.currentState.parent.children[next_index]
            # make the move to actually update the KB to the sibling state
            self.gm.makeMove(self.currentState.requiredMovable)
        # while the current state is not visited and there are children, we want to move down the tree
        while self.visited.get(self.currentState, False) and self.currentState.children:
            firstChild = 0
            # go down the tree using the left most child - therefore, i used the 0 index
            self.currentState = self.currentState.children[firstChild]
            # make move to update the KB
            self.gm.makeMove(self.currentState.requiredMovable)
        # search any unvisited nodes
        if self.visited.get(self.currentState, False):
            self.search()
        return True

    def getIndex(self, state):
        index = state.parent.children.index(state)
        return index
