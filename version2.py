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
        self.best_definite = False
        tree.nodes += 1
        self.legal_moves = list(position.generate_legal_moves())
        self.priority = 0

    def gen_branches(self, target_depth, time_start=None):
        self.best_definite = False
        if target_depth == self.depth + 1:
            evals = []
            for i, move in enumerate(self.legal_moves):
                new_board = deepcopy(self.position)
                new_board.push(move)
                new_node = Node(new_board, self.tree, self, self.depth+1)
                self.branches.append(new_node)
                evals.append((evaluate(new_board), i))
                if not self.tree.active:
                    return

            if len(evals) > 15:
                evals = sorted(evals, key=lambda x: x[0])
                num_first = max(len(evals)//5, 4)
                num_second = min(len(evals)//2, 11)
                for branch in self.branches[:num_first]:
                    branch.priority = 0
                for branch in self.branches[num_first:num_second]:
                    branch.priority = 1
                for branch in self.branches[num_second:]:
                    branch.priority = 2

            self.minimax()
            self.set_indefinite()

        elif target_depth > self.depth + 1:
            for i, data in enumerate(zip(self.branches, self.legal_moves)):
                branch, move = data
                if self.depth == 0:
                    time_elapse = time.time() - time_start
                    print(f"info depth {target_depth} currmove {move.uci()} currmovenumber {i+1} nodes {self.tree.nodes} nps {int(self.tree.nodes/time_elapse)} time {int(time_elapse*1000)}", flush=True)
                branch.gen_branches(target_depth)

                if not self.tree.active:
                    return

    def minimax(self):
        self.best_definite = True
        if len(self.branches) == 0:
            prev_move = None if len(self.position.move_stack) == 0 else self.position.peek()
            self.eval = evaluate(self.position)
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
                evaluation = branch.get_best()[0]
                if evaluation > max_eval:
                    max_eval = evaluation
                    best_move = branch.position.peek()
                    best_ind = i

            self.eval = max_eval
            self.best = [best_move] + self.branches[best_ind].best
            return (max_eval, best_move)

        else:
            min_eval = float("inf")
            best_move = None
            best_ind = 0
            for i, branch in enumerate(self.branches):
                evaluation = branch.get_best()[0]
                if evaluation < min_eval:
                    min_eval = evaluation
                    best_move = branch.position.peek()
                    best_ind = i

            self.eval = min_eval
            self.best = [best_move] + self.branches[best_ind].best
            return (min_eval, best_move)

    def get_best(self):
        if self.best_definite:
            return (self.eval, self.best)
        else:
            self.minimax()
            return (self.eval, self.best)

    def set_indefinite(self):
        self.best_definite = False
        if self.parent is not None:
            self.parent.set_indefinite()


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
        self.position = kwargs["position"]
        self.root = Node(kwargs["position"], self, None, 0)

        final_depth = 99
        if "depth" in kwargs:
            final_depth = kwargs["depth"]
        elif "nodes" in kwargs:
            threading.Thread(target=self.timer_nodes, args=(kwargs["nodes"],)).start()
            final_depth = 99
        elif "wtime" in kwargs or "btime" in kwargs:
            move_time = self.calc_move_time(kwargs)
            threading.Thread(target=self.timer_time, args=(move_time,)).start()
            final_depth = 99
        elif "movetime" in kwargs:
            move_time = kwargs["movetime"] / 1000
            threading.Thread(target=self.timer_time, args=(move_time,)).start()
            final_depth = 99

        #threading.Thread(target=self.periodic_print).start()
        for depth in range(final_depth+1):
            self.print_info()
            self.depth = depth
            self.root.gen_branches(depth, self.time_start)
            if not self.active:
                break

        self.print_info(force=True)
        print("bestmove " + self.root.get_best()[1][0].uci(), flush=True)

    def timer_nodes(self, nodes):
        while self.nodes < nodes:
            time.sleep(0.01)
        self.active = False

    def timer_time(self, total_time):
        time_end = time.time() + total_time
        while time.time() < time_end:
            time.sleep(0.01)
        self.active = False

    def calc_move_time(self, kwargs):
        return 5

    def periodic_print(self):
        base = 30000
        inc = 200
        mult = 0
        while self.active:
            next_num = mult * base
            while self.nodes < next_num:
                time.sleep(0.01)
                if not self.active:
                    return
            
            threading.Thread(target=self.print_info).start()
            base += inc
            mult += 1

    def print_info(self, force=False):
        info = self.root.get_best()
        self.score = info[0]
        self.moves = " ".join([move.uci() for move in info[1][:-1] if move is not None])
        if self.score > 1000000:
            mate_in = (abs(16777216 - self.score) + 1) // 2
            score = f"mate +{mate_in}"
        elif self.score < -1000000:
            mate_in = (abs(16777216 + self.score) + 1) // 2
            score = f"mate -{mate_in}"
        else:
            score = f"cp {self.score}" if self.position.turn else f"cp {-1 * self.score}"

        time_elapse = time.time() - self.time_start + 0.01
        info_str = self.info_str.format(depth=self.depth, score=score, nodes=self.nodes, nps=int(self.nodes/time_elapse), time=int(time_elapse*1000), moves=self.moves)
        if self.active or force:
            print(info_str, flush=True)


def evaluate(position: chess.Board):
    if position.is_game_over():
        result = position.result()
        if result == "1-0":
            return float("inf")
        elif result == "0-1":
            return float("-inf")
        elif result == "1/2-1/2":
            return 0

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