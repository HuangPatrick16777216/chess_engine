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
    def __init__(self, root, position, depth):
        self.root = root
        self.position = position
        self.depth = depth
        
        self.evaluation = None
        self.branches = []
        root.nodes += 1

    def gen_branches(self, target_depth):
        if target_depth == self.depth + 1:
            for move in self.position.generate_legal_moves():
                new_board = deepcopy(self.position)
                new_board.push(move)
                self.branches.append(Node(self.root, new_board, self.depth+1))
                if not self.root.active:
                    return
        
        else:
            for branch in self.branches:
                branch.gen_branches(target_depth)
                if not self.root.active:
                    return

    def minimax(self):
        if len(self.branches) == 0:
            if len(self.position.move_stack) == 0:
                return (self.evaluate(), None)
            else:
                return (self.evaluate(), self.position.peek())
        else:
            if self.position.turn:
                max_eval = float("-inf")
                best_move = None
                for branch in self.branches:
                    curr_eval = branch.minimax()[0]
                    if curr_eval > max_eval:
                        max_eval = curr_eval
                        if self.depth == 0:
                            best_move = branch.position.peek()
                    if not self.root.active:
                        break

                return (max_eval, best_move)

            else:
                min_eval = float("inf")
                best_move = None
                for branch in self.branches:
                    curr_eval = branch.minimax()[0]
                    if curr_eval < min_eval:
                        min_eval = curr_eval
                        if self.depth == 0:
                            best_move = branch.position.peek()
                    if not self.root.active:
                        break

                return (min_eval, best_move)
    
    def evaluate(self):
        if self.evaluation is not None:
            return self.evaluation
        
        mat_weight = 1

        # Material, more aspects added later
        material = 0
        pieces = self.position.fen()
        material += pieces.count("P") - pieces.count("p")
        material += 3 * (pieces.count("N") - pieces.count("n"))
        material += 3 * (pieces.count("B") - pieces.count("b"))
        material += 5 * (pieces.count("R") - pieces.count("r"))
        material += 9 * (pieces.count("Q") - pieces.count("q"))

        score = material*mat_weight
        self.evaluation = score
        return score


class Tree:
    info_str = "info depth {depth} seldepth {depth} multipv 1 score cp {score} nodes {nodes} nps {nps} tbhits 0 time {time} pv {moves}"

    def init_vars(self):
        self.curr_depth = 0
        self.curr_score = 0
        self.nodes = 0
        self.curr_move = None
        self.time_start = time.time()

    def search(self, **kwargs):
        self.active = True
        self.init_vars()
        self.root = Node(self, kwargs["position"], 0)
        
        threading.Thread(target=self.periodic_printer).start()
        if "depth" in kwargs:
            for depth in range(kwargs["depth"]+1):
                self.curr_depth = depth
                self.print_info()
                self.root.gen_branches(depth)
                if not self.active:
                    break
        
        self.print_info()
        self.print_best_move()

    def periodic_printer(self):
        base = 2500
        base_inc = 125
        curr_mult = 0
        while self.active:
            next_val = curr_mult * base
            while self.nodes < next_val:
                time.sleep(0.01)
                if not self.active:
                    return
            
            threading.Thread(target=self.print_info).start()
            curr_mult += 1
            base += base_inc

    def print_info(self):
        self.curr_move = self.root.minimax()[1]
        curr_time = time.time()
        info_str = self.info_str.format(depth=self.curr_depth, score=self.curr_score, nodes=self.nodes, nps=int(self.nodes/(curr_time-self.time_start+0.01)),
            time=int((curr_time-self.time_start)*1000), moves=self.curr_move)
        print(info_str)

    def print_best_move(self):
        print(f"bestmove {self.curr_move.uci()}")


def main():
    position = chess.Board()
    tree = Tree()

    while True:
        msg = input().strip()

        if msg == "quit":
            tree.active = False
            return
        elif msg == "isready":
            print("readyok")
        elif msg == "uci":
            print("uciok")
        elif msg == "d":
            print(position)

        elif msg.startswith("position"):
            msg = msg.replace("position", "").strip()

            if msg.startswith("startpos"):
                msg = msg.replace("startpos", "").strip()
                position = chess.Board()

                if msg.startswith("moves"):
                    for move in msg.replace("moves", "").strip().split(" "):
                        position.push_uci(move)

            elif msg.startswith("fen"):
                fen = msg.replace("fen", "").strip()
                position = chess.Board(fen)

        elif msg.startswith("go"):
            threading.Thread(target=tree.search, kwargs={"position": position, "depth": 5}).start()
        elif msg == "stop":
            tree.active = False


main()