
from solver import *
import pdb

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
        # self.unwalk()
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
                # self.visited[newState] = True
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
        # Student code goes here
        return True
