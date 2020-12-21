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

import time
import threading
import chess
from copy import deepcopy


class Node:
    def __init__(self, position: chess.Board, depth, tree):
        self.position = position
        self.depth = depth
        self.tree = tree
        self.branches = []

        tree.nodes += 1
        self.eval = evaluate(position)
        self.priority = None

    def gen_branches(self, target_depth):
        if not self.tree.active:
            return

        if target_depth == self.depth + 1:
            for move in self.position.generate_legal_moves():
                new_board = deepcopy(self.position)
                new_board.push(move)
                new_node = Node(new_board, self.depth+1, self.tree)
                self.branches.append(new_node)

        elif target_depth > self.depth + 1:
            if self.depth == 0:
                for i, move, branch in zip(range(len(self.branches)), list(self.position.generate_legal_moves()), self.branches):
                    if self.tree.active:
                        print(f"info depth {target_depth} currmove {move.uci()} currmovenumber {i}", flush=True)
                    branch.gen_branches(target_depth)
            else:
                for branch in self.branches:
                    branch.gen_branches(target_depth)


class Tree:
    def init_vars(self):
        self.active = True
        self.nodes = 0
        self.bestmove = None
        self.eval = 0
        self.time_start = time.time()

    def search(self, **kwargs):
        self.init_vars()
        position = kwargs["position"]
        self.root = Node(position, 0, self)

        for depth in range(100):
            self.root.gen_branches(depth)


def evaluate(position):
    if position.is_game_over():
        result = position.result()
        if result == "1-0":
            return float("inf")
        elif result == "0-1":
            return float("-inf")
        elif result == "1/2-1/2":
            return 0

    
    # General
    pieces = position.fen().split(" ")[0]
    pieces_remaining = {
        "P": pieces.count("P"), "p": pieces.count("p"),
        "N": pieces.count("N"), "n": pieces.count("n"),
        "B": pieces.count("B"), "b": pieces.count("b"),
        "R": pieces.count("R"), "r": pieces.count("r"),
        "Q": pieces.count("Q"), "q": pieces.count("q")
    }

    # Material
    material = 0
    material += pieces_remaining["P"] - pieces_remaining["p"]
    material += 3 * (pieces_remaining["N"] - pieces_remaining["n"])
    material += 3 * (pieces_remaining["B"] - pieces_remaining["b"])
    material += 5 * (pieces_remaining["R"] - pieces_remaining["r"])
    material += 9 * (pieces_remaining["Q"] - pieces_remaining["q"])
    

    score = material
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


main()