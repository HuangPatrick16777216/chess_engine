#
#  Chess Engine
#  UCI chess engine
#  Copyright Patrick Huang 2021
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.
#

import time
import threading
import chess
from copy import deepcopy
from eval import evaluate


class Tree:
    print_str = "info depth {} seldepth {} multipv 1 score {} nodes {} nps {} tbhits 0 time {} pv {}"

    def __init__(self):
        self.init_vars(chess.Board())

    def init_vars(self, board):
        self.active = True
        self.board = board
        self.nodes = 0
        self.depth = 0
        self.time_start = time.time()

    def go(self, **kwargs):
        self.init_vars(kwargs["board"])
        self.root = Node(kwargs["board"], 0, self)
        threading.Thread(target=self.printer).start()

        for depth in range(4):
            self.depth = depth
            self.root.branch(depth)

        self.active = False
        self.print_best()

    def printer(self):
        while self.active:
            elapse = time.time() - self.time_start
            string = self.print_str.format(self.depth, self.depth, self.root.eval, self.nodes,
                int(self.nodes/elapse), int(elapse*1000), self.root.best)
            print(string, flush=True)
            time.sleep(1)

    def print_best(self):
        print(f"bestmove {self.root.best}", flush=True)


class Node:
    def __init__(self, board: chess.Board, depth, tree: Tree):
        self.board = board
        self.depth = depth
        self.tree = tree
        self.children = []

        self.eval = evaluate(board)
        self.best = None

    def branch(self, target_depth):
        if target_depth == self.depth+1:
            for move in self.board.generate_legal_moves():
                new_board = deepcopy(self.board)
                new_board.push(move)
                new_node = Node(self.board, self.depth+1, self.tree)

                self.children.append(new_node)
                self.tree.nodes += 1

        elif target_depth > self.depth+1:
            for c in self.children:
                c.branch(target_depth)
