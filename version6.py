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
        self.priority = "HIGH"
        self.best_definite = False

    def gen_branches(self, target_depth):
        self.best_definite = False
        if not self.tree.active:
            return

        if self.priority == "MED":
            target_depth = int(target_depth * MED_FAC)
        elif self.priority == "LOW":
            target_depth = int(target_depth * LOW_SPEED)

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
                        self.tree.print_info()
                    branch.gen_branches(target_depth)
            else:
                for branch in self.branches:
                    branch.gen_branches(target_depth)
            if target_depth == self.depth + 3:
                self.prioritize()
    
    def minimax(self):
        if self.best_definite:
            return (self.eval, self.best)

        self.best_definite = True
        if len(self.branches) == 0:
            prev_move = None if len(self.position.move_stack) == 0 else self.position.peek()
            if self.eval == float("inf"):
                self.eval = 16777216 - self.depth
            elif self.eval == float("-inf"):
                self.eval = -16777216 + self.depth

            self.best = [prev_move]
            return (self.eval, self.best)

        if self.position.turn:
            max_eval = float("-inf")
            best_move = None
            best_ind = 0
            for i, branch in enumerate(self.branches):
                evaluation = branch.minimax()[0]
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = branch.position.peek()
                    best_ind = i

            self.eval = max_eval
            self.best = [best_move] + self.branches[best_ind].best
            return (self.eval, self.best)

        else:
            min_eval = float("inf")
            best_move = None
            best_ind = 0
            for i, branch in enumerate(self.branches):
                evaluation = branch.minimax()[0]
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = branch.position.peek()
                    best_ind = i

            self.eval = min_eval
            self.best = [best_move] + self.branches[best_ind].best
            return (self.eval, self.best)
            
    def prioritize(self):
        length = len(self.branches)
        if not length > 15:
            return

        evals = [(b, b.minimax()[0], i) for i, b in enumerate(self.branches)]
        evals = sorted(evals, key=(lambda x: x[1]))
        if self.position.turn:
            evals = reversed(evals)
        
        split1 = int(length*HIGH_FAC)
        split2 = int(length*HIGH_FAC + length*MED_FAC)
        high, med, low = [], [], []
        for i in range(length):
            if i < split1:
                high.append(i)
            else:
                med.append(i) if i < split2 else low.append(i)

        for i in high:
            self.branches[i].priority = "HIGH"
        for i in med:
            self.branches[i].priority = "MED"
        for i in low:
            self.branches[i].priority = "LOW"


class Tree:
    info_str = "info depth {depth} seldepth {seldepth} multipv 1 score {score} nodes {nodes} nps {nps} tbhits 0 time {time} pv {moves}"

    def init_vars(self):
        self.active = True
        self.nodes = 0
        self.eval = 0
        self.depth = 0
        self.bestmove = None
        self.time_start = time.time()

    def search(self, **kwargs):
        self.init_vars()
        position = kwargs["position"]
        self.root = Node(position, 0, self)

        for depth in range(100):
            self.depth = depth
            self.root.gen_branches(depth)

    def print_info(self):
        time_elapse = time.time() - self.time_start
        print_str = self.info_str.format(depth=self.depth, seldepth=self.depth, score=self.eval, nodes=self.nodes,
            nps=int(self.nodes/time_elapse), time=int(time_elapse*1000), moves=None)
        print(print_str, flush=True)


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


HIGH_FAC = 0.3
MED_FAC = 0.3
MED_SPEED = 0.7
LOW_SPEED = 0.3
main()