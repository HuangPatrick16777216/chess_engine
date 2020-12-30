#  ##### BEGIN GPL LICENSE BLOCK #####
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
# ##### END GPL LICENSE BLOCK #####

import chess
import threading
import time
from copy import deepcopy


class Node:
    def __init__(self, position, depth, tree):
        self.position = position
        self.depth = depth
        self.tree = tree

        self.branches = []
        self.eval = None
        self.best = None
        self.best_definite = False
        self.tree.nodes += 1

    def gen_branches(self, target_depth):
        self.best_definite = False
        if target_depth == self.depth + 1:
            for i, move in enumerate(self.position.generate_legal_moves()):
                new_board = deepcopy(self.position)
                new_board.push(move)
                new_node = Node(new_board, self.depth + 1, self.tree)
                self.branches.append((i, new_node))
                if not self.tree.active:
                    return

        elif target_depth > self.depth + 1:
            for branch in self.branches:
                branch[1].gen_branches(target_depth)
                if not self.tree.active:
                    return

    def minimax(self):
        self.best_definite = True
        if len(self.branches) == 0:
            self.eval = evaluate(self.position)
            self.best = None
            return (self.eval, self.best)

        if self.position.turn:
            self.eval = float("inf")
            self.best = None
            for branch in self.branches:
                eval_info = branch.minimax()


def evaluate(position):
    return 0


class Tree:
    def init_vars(self):
        self.active = True
        self.nodes = 0
        self.time_start = time.time()

    def search(self, **kwargs):
        self.root = Node(kwargs["position"], 0, self)
        self.init_vars()


def main():
    position = chess.Board()
    tree = Tree()

    while True:
        msg = input().strip()

        if msg == "quit":
            return
        elif msg == "isready":
            print("readyok", flush=True)
        elif msg == "uci":
            print("uciok", flush=True)
        elif msg == "d":
            print(position, flush=True)

        elif msg == "ucinewgame":
            position = chess.Board()
        elif msg.startswith("position"):
            msg = msg.replace("position", "").strip()
            if msg.startswith("startpos"):
                msg = msg.replace("startpos", "").strip()
                position = chess.Board()
                if msg.startswith("moves"):
                    moves = msg.replace("moves", "").strip().split(" ")
                    for move in moves:
                        position.push_uci(move)

            elif msg.startswith("fen"):
                fen = msg.replace("fen", "").strip()
                position = chess.Board(fen)

        elif msg.startswith("go"):
            msg = msg.replace("go", "").strip()
            kwargs = {"position": position}

            if msg.startswith("nodes"):
                kwargs["nodes"] = int(msg.replace("nodes", "").strip())
            elif msg.startswith("depth"):
                kwargs["depth"] = int(msg.replace("depth", "").strip())
            elif msg.startswith("movetime"):
                kwargs["movetime"] = int(msg.replace("movetime", "").strip())
            elif "wtime" in msg or "btime" in msg:
                parts = msg.split(" ")
                for i in range(0, len(parts)//2):
                    kwargs[parts[i*2]] = int(parts[i*2+1]) / 1000

            threading.Thread(target=tree.search, kwargs=kwargs).start()
        elif msg == "stop":
            tree.active = False