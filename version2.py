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
        self.eval = None
        self.best = None
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
            for i, data in enumerate(zip(self.branches, self.position.generate_legal_moves())):
                if not self.tree.active:
                    return

                branch, move = data
                branch.gen_branches(target_depth)
                if self.depth == 0:
                    print(f"info depth {target_depth} currmove {move.uci()} currmovenumber {i+1}")

    def minimax(self):
        if len(self.branches) == 0:
            prev_move = None if len(self.position.move_stack) == 0 else self.position.peek()
            return (evaluate(), prev_move)

        if self.position.turn:
            max_eval = float("-inf")
            best_move = None
            for branch in self.branches:
                evaluation = branch.evaluate()[0]
                if evaluation >= max_eval:
                    max_eval = evaluation
                    best_move = branch.position.peek()
            return (max_eval, best_move)

        else:
            min_eval = float("inf")
            best_move = None
            for branch in self.branches:
                evaluation = branch.evaluate[0]
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = branch.position.peek()
            return (min_eval, best_move)


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
        self.init_vars()
        self.root = Node(kwargs["position"], self, None, 0)

        threading.Thread(target=self.periodic_print).start()
        for depth in range(99):
            self.print_info()
            self.depth = depth
            self.root.gen_branches(depth)
            if not self.active:
                break

        self.print_info()

    def periodic_print(self):
        base = 7500
        inc = 200
        mult = 0
        while self.active:
            next_num = mult * base
            while self.nodes < next_num:
                time.sleep(0.01)
                if not self.active:
                    return
            
            self.print_info()
            base += inc
            mult += 1

    def print_info(self):
        time_elapse = time.time() - self.time_start + 0.01
        score = f"cp {self.score}"
        info_str = self.info_str.format(depth=self.depth, score=score, nodes=self.nodes, nps=int(self.nodes/time_elapse), time=int(time_elapse*1000), moves=self.moves)
        print(info_str, flush=True)


def evaluate(position):
    pieces = position.fen().split(" ")[0]
    pieces_remaining = {
        "P": pieces.count("P"), "p": pieces.count("p"),
        "N": pieces.count("N"), "n": pieces.count("n"),
        "B": pieces.count("B"), "b": pieces.count("b"),
        "R": pieces.count("R"), "r": pieces.count("r"),
        "Q": pieces.count("Q"), "q": pieces.count("q")
    }
    #total_pieces = sum([pieces_remaining[key] for key in pieces_remaining])

    material = 0
    material += pieces_remaining["P"] - pieces_remaining["p"]
    material += 3 * (pieces_remaining["N"] - pieces_remaining["n"])
    material += 3 * (pieces_remaining["B"] - pieces_remaining["b"])
    material += 5 * (pieces_remaining["R"] - pieces_remaining["r"])
    material += 9 * (pieces_remaining["Q"] - pieces_remaining["q"])

    score = 1 * material
    return 100 * score


def main():
    position = chess.Board()
    tree = Tree()

    while True:
        msg = input().strip()
        
        if msg == "quit":
            tree.active = False
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
            threading.Thread(target=tree.search, kwargs={"position": position}).start()
        elif msg == "stop":
            tree.active = False


main()