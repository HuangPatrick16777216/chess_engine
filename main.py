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

import sys
import time
import threading
import chess
from copy import deepcopy


class Node:
    def __init__(self, root, position: chess.Board, depth):
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

        if self.position.is_game_over():
            result = self.position.result()
            if result == "1-0":
                score = 16777216 * (self.depth+1)
                self.evaluation = score
                return score
            elif result == "0-1":
                score = -16777216 * (self.depth+1)
                self.evaluation = score
                return score
            elif result == "1/2-1/2":
                self.evaluation = 0
                return 0
        
        mat_weight = 1

        # Material
        material = 0
        pieces = self.position.fen()
        material += pieces.count("P") - pieces.count("p")
        material += 3 * (pieces.count("N") - pieces.count("n"))
        material += 3 * (pieces.count("B") - pieces.count("b"))
        material += 5 * (pieces.count("R") - pieces.count("r"))
        material += 9 * (pieces.count("Q") - pieces.count("q"))

        score = material*mat_weight
        score *= 100
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
        total_depth = 99
        if "depth" in kwargs:
            total_depth = kwargs["depth"] + 1
        elif "nodes" in kwargs:
            threading.Thread(target=self.timer_nodes, args=(kwargs["nodes"],)).start()
        elif "time" in kwargs:
            threading.Thread(target=self.timer_time, args=(kwargs["time"],)).start()
        elif "wtime" in kwargs or "btime" in kwargs:
            total_time = self.calc_optimal_time(kwargs)
            threading.Thread(target=self.timer_time, args=(total_time,)).start()

        for depth in range(total_depth):
            self.curr_depth = depth
            self.print_info()
            self.root.gen_branches(depth)
            if not self.active:
                break
        
        self.print_info()
        self.active = False
        time.sleep(0.05)
        self.print_best_move()

    def calc_optimal_time(self, time_info):
        # todo calculate
        return 10

    def timer_nodes(self, nodes):
        while self.nodes < nodes:
            time.sleep(0.01)
        self.active = False

    def timer_time(self, total_time):
        time_end = time.time() + total_time
        while time.time() < time_end:
            time.sleep(0.01)
        self.active = False

    def periodic_printer(self):
        base = 15000
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
        eval_info = self.root.minimax()
        self.curr_score = eval_info[0]
        self.curr_move = eval_info[1]
        curr_time = time.time()
        info_str = self.info_str.format(depth=self.curr_depth, score=self.curr_score, nodes=self.nodes, nps=int(self.nodes/(curr_time-self.time_start+0.01)),
            time=int((curr_time-self.time_start)*1000), moves=self.curr_move)
        if self.active:
            print(info_str, flush=True)

    def print_best_move(self):
        print(f"bestmove {self.curr_move.uci()}", flush=True)


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

        elif msg.startswith("ucinewgame"):
            position = chess.Board()
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
            msg = msg.replace("go", "").strip()
            kwargs = {"position": position}

            if msg.startswith("depth"):
                depth = int(msg.replace("depth", "").strip())
                kwargs["depth"] = depth
            elif msg.startswith("nodes"):
                nodes = int(msg.replace("nodes", "").strip())
                kwargs["nodes"] = nodes
            elif msg.startswith("movetime"):
                time = int(msg.replace("movetime", "").strip()) / 1000
                kwargs["time"] = time
            elif ("wtime" in msg and position.turn) or ("btime" in msg and not position.turn):
                parts = msg.split(" ")
                for i in range(0, len(parts)//2):
                    kwargs[parts[i*2]] = int(parts[i*2+1]) / 1000
            else:
                kwargs["depth"] = 99

            threading.Thread(target=tree.search, kwargs=kwargs).start()
        elif msg == "stop":
            tree.active = False


main()