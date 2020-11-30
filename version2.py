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

import threading
import time
import chess
from copy import deepcopy


class Node:
    def __init__(self, position, tree, parent, depth):
        self.position = position
        self.tree = tree
        self.parent = parent
        self.depth = depth

        self.branches = []
        tree.nodes += 1

    def gen_branches(self, target_depth):
        if target_depth == self.depth + 1:
            for move in self.position.generate_legal_moves():
                new_board = deepcopy(self.position)
                new_board.push(move)
                new_node = Node(new_board, self.tree, self, self.depth+1)
                self.branches.append(new_node)
                if not self.tree.active:
                    return

        elif target_depth > self.depth + 1:
            for branch in self.branches:
                branch.gen_branches(target_depth)
                if not self.tree.active:
                    return


class Tree:
    info_str = "info depth {depth} seldepth {depth} multipv 1 score {score} nodes {nodes} nps {nps} tbhits 0 time {time} pv {moves}"
    def __init__(self):
        self.init_vars()

    def init_vars(self):
        self.nodes = 0
        self.depth = 0
        self.score = 0
        self.moves = []
        self.active = True
        self.time_start = time.time()

    def search(self, **kwargs):
        self.root = Node(kwargs["position"], self, None, 0)
        for depth in range(5):
            self.print_info()
            self.depth = depth
            self.root.gen_branches(depth)

    def print_info(self):
        time_elapse = time.time() - self.time_start
        score = f"cp {self.score}"
        info_str = self.info_str.format(depth=self.depth, score=score, nodes=self.nodes, nps=int(self.nodes/time_elapse), time=int(time_elapse*1000), moves=self.moves)
        print(info_str, flush=True)


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
            print(position)

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
            threading.Thread(target=tree.search, kwargs={"position": position}).start()
        elif msg == "stop":
            tree.active = False


main()