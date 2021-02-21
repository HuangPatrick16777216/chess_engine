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
import chess
from copy import deepcopy


class Tree:
    def __init__(self):
        self.init_vars(chess.Board())

    def init_vars(self, board):
        self.active = False
        self.board = board
        self.nodes = 0
        self.time_start = time.time()

    def go(self, **kwargs):
        self.init_vars(kwargs["board"])
        self.root = Node(kwargs["board"], 0, self)
        for depth in range(4):
            self.root.branch(depth)


class Node:
    def __init__(self, board, depth, tree):
        self.board = board
        self.depth = depth
        self.tree = tree
        self.children = []

    def branch(self, target_depth):
        if self.depth+1 == target_depth:
            for move in self.board.generate_legal_moves():
                new_board = deepcopy(self.board)
                new_board.push(move)
                new_node = Node(self.board, self.depth+1, self.tree)

                self.children.append(new_node)
                self.tree.nodes += 1
