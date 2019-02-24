from game_master import GameMaster
from read import *
from util import *


class TowerOfHanoiGame(GameMaster):

    def __init__(self):
        super().__init__()
        
    def produceMovableQuery(self):
        """
        See overridden parent class method for more information.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?disk ?init ?target)')

    def getGameState(self):
        """
        Returns a representation of the game in the current state.
        The output should be a Tuple of three Tuples. Each inner tuple should
        represent a peg, and its content the disks on the peg. Disks
        should be represented by integers, with the smallest disk
        represented by 1, and the second smallest 2, etc.

        Within each inner Tuple, the integers should be sorted in ascending order,
        indicating the smallest disk stacked on top of the larger ones.

        For example, the output should adopt the following format:
        ((1,2,5),(),(3, 4))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ## student code goes here

        onpeg1 = self.kb.kb_ask(parse_input("fact: (on ?X peg1)"))
        onpeg2 = self.kb.kb_ask(parse_input("fact: (on ?X peg2)"))
        onpeg3 = self.kb.kb_ask(parse_input("fact: (on ?X peg3)"))

        peg1tuple = []
        peg2tuple = []
        peg3tuple = []

        if onpeg1:
            for i in range(len(onpeg1)):
                for binding in onpeg1[i].bindings:
                    string = str(binding.constant)
                    index = len(string)
                    peg1tuple.append(int(string[index - 1]))
            peg1tuple.sort()

        if onpeg2:
            for i in range(len(onpeg2)):
                for binding in onpeg2[i].bindings:
                    string = str(binding.constant)
                    index = len(string)
                    peg2tuple.append(int(string[index - 1]))
            peg2tuple.sort()

        if onpeg3:
            for i in range(len(onpeg3)):
                for binding in onpeg3[i].bindings:
                    string = str(binding.constant)
                    index = len(string)
                    peg3tuple.append(int(string[index - 1]))
            peg3tuple.sort()

        gameState = (tuple(peg1tuple), tuple(peg2tuple), tuple(peg3tuple))

        # print(gameState)
        return gameState

        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable disk1 peg1 peg3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        term = movable_statement.terms
        disk = str(term[0])
        oldp = str(term[1])
        newp = str(term[2])

        # retract the Top of the old peg
        retractTop = "fact: (Top " + disk + " " + oldp + ")"
        self.kb.kb_retract(parse_input(retractTop))

        under = "fact: (onTop " + disk + " ?X)"
        underAns = self.kb.kb_ask(parse_input(under))
        emptyTop = "fact: (empty " + oldp + ")"

        if underAns:
            # print("under moving disk")
            # print(underAns[0].bindings[0].constant)
            retractonTop = "fact: (onTop " + disk + " " + str(underAns[0].bindings[0].constant) + ")"
            self.kb.kb_retract(parse_input(retractonTop))
            addNewTop = "fact: (Top " + str(underAns[0].bindings[0].constant) + " " + oldp + ")"
            self.kb.kb_assert(parse_input(addNewTop))
        else:
            # print("under moving disk")
            # print(False)
            self.kb.kb_assert(parse_input(emptyTop))

        retractOn = "fact: (on " + disk + " " + oldp + ")"
        self.kb.kb_retract(parse_input(retractOn))

        # new peg updates
        # set new top
        under2 = "fact: (Top ?X " + newp + ")"
        under2Ans = self.kb.kb_ask(parse_input(under2))

        # if there was a top, retract it before adding new top
        if under2Ans:
            # print("top of target peg:")
            # print(under2Ans[0].bindings[0].constant)
            retractTop2 = "fact: (Top " + str(under2Ans[0].bindings[0].constant) + " " + newp + ")"
            self.kb.kb_retract(parse_input(retractTop2))
            addonTopNew = "fact: (onTop " + disk + " " + str(under2Ans[0].bindings[0].constant) + ")"
            self.kb.kb_assert(parse_input(addonTopNew))
        else:
            # print("top of target peg:")
            # print(False)
            emptyremove = "fact: (empty " + newp + ")"
            self.kb.kb_retract(parse_input(emptyremove))

        # add disk to new peg
        addOn = "fact: (on " + disk + " " + newp + ")"
        self.kb.kb_assert(parse_input(addOn))

        addTop = "fact: (Top " + disk + " " + newp + ")"
        self.kb.kb_assert(parse_input(addTop))


    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[2], sl[1]]
        self.makeMove(Statement(newList))

class Puzzle8Game(GameMaster):

    def __init__(self):
        super().__init__()

    def produceMovableQuery(self):
        """
        Create the Fact object that could be used to query
        the KB of the presently available moves. This function
        is called once per game.

        Returns:
             A Fact object that could be used to query the currently available moves
        """
        return parse_input('fact: (movable ?piece ?initX ?initY ?targetX ?targetY)')

    def getGameState(self):
        """
        Returns a representation of the the game board in the current state.
        The output should be a Tuple of Three Tuples. Each inner tuple should
        represent a row of tiles on the board. Each tile should be represented
        with an integer; the empty space should be represented with -1.

        For example, the output should adopt the following format:
        ((1, 2, 3), (4, 5, 6), (7, 8, -1))

        Returns:
            A Tuple of Tuples that represent the game state
        """
        ### Student code goes here

        row1 = self.kb.kb_ask(parse_input("fact: (location ?X ?pos pos1)"))
        row2 = self.kb.kb_ask(parse_input("fact: (location ?X ?pos pos2)"))
        row3 = self.kb.kb_ask(parse_input("fact: (location ?X ?pos pos3)"))

        row1tuple = [-1, -1, -1]
        row2tuple = [-1, -1, -1]
        row3tuple = [-1, -1, -1]

        for i in range(len(row1)):
            tile = str(row1[i].bindings[0].constant)
            pos = str(row1[i].bindings[1].constant)
            tilenum = tile[len(tile) - 1]
            posnum = int(pos[len(pos) - 1])

            if tilenum == "y":
                row1tuple[posnum - 1] = -1
            else:
                row1tuple[posnum - 1] = int(tilenum)

        for i in range(len(row2)):
            tile = str(row2[i].bindings[0].constant)
            pos = str(row2[i].bindings[1].constant)
            tilenum = tile[len(tile) - 1]
            posnum = int(pos[len(pos) - 1])

            if tilenum == "y":
                row2tuple[posnum - 1] = -1
            else:
                row2tuple[posnum - 1] = int(tilenum)

        for i in range(len(row3)):
            tile = str(row3[i].bindings[0].constant)
            pos = str(row3[i].bindings[1].constant)
            tilenum = tile[len(tile) - 1]
            posnum = int(pos[len(pos) - 1])

            if tilenum == "y":
                row3tuple[posnum - 1] = -1
            else:
                row3tuple[posnum - 1] = int(tilenum)

        gameState = (tuple(row1tuple), tuple(row2tuple), tuple(row3tuple))

        return gameState

        pass

    def makeMove(self, movable_statement):
        """
        Takes a MOVABLE statement and makes the corresponding move. This will
        result in a change of the game state, and therefore requires updating
        the KB in the Game Master.

        The statement should come directly from the result of the MOVABLE query
        issued to the KB, in the following format:
        (movable tile3 pos1 pos3 pos2 pos3)

        Args:
            movable_statement: A Statement object that contains one of the currently viable moves

        Returns:
            None
        """
        ### Student code goes here

        term = movable_statement.terms

        tile_name = str(term[0])
        posxi = str(term[1])
        posyi = str(term[2])
        posxt = str(term[3])
        posyt = str(term[4])

        retract = "fact: (location " + tile_name + " " + posxi + " " + posyi + ")"
        add = "fact: (location " + tile_name + " " + posxt + " " + posyt + ")"
        retractempty = "fact: (location empty " + posxt + " " + posyt + ")"
        addempty = "fact: (location empty" + " " + posxi + " " + posyi + ")"

        self.kb.kb_retract(parse_input(retract))
        self.kb.kb_retract(parse_input(retractempty))
        self.kb.kb_assert(parse_input(add))
        self.kb.kb_assert(parse_input(addempty))

        pass

    def reverseMove(self, movable_statement):
        """
        See overridden parent class method for more information.

        Args:
            movable_statement: A Statement object that contains one of the previously viable moves

        Returns:
            None
        """
        pred = movable_statement.predicate
        sl = movable_statement.terms
        newList = [pred, sl[0], sl[3], sl[4], sl[1], sl[2]]
        self.makeMove(Statement(newList))
