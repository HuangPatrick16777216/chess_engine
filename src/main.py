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

import threading
import chess
from tree import Tree


def main():
    board = chess.Board()
    tree = Tree()

    while True:
        try:
            msg = input().strip()
        except EOFError:
            return

        if msg == "quit":
            tree.active = False
            return
        elif msg == "isready":
            print("readyok", flush=True)
        elif msg == "uci":
            print("uciok", flush=True)
        elif msg == "d":
            print(board, flush=True)

        elif msg == "ucinewgame":
            board = chess.Board()
        elif msg.startswith("position"):
            msg = msg.replace("position", "").strip()
            if msg.startswith("startpos"):
                msg = msg.replace("startpos", "").strip()
                board = chess.Board()
                if msg.startswith("moves"):
                    moves = msg.replace("moves", "").strip().split(" ")
                    for move in moves:
                        board.push_uci(move)

            elif msg.startswith("fen"):
                fen = msg.replace("fen", "").strip()
                board = chess.Board(fen)

        elif msg.startswith("go"):
            msg = msg.replace("go", "").strip()
            kwargs = {"board": board}

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

            threading.Thread(target=tree.go, kwargs=kwargs).start()

        elif msg == "stop":
            tree.active = False


main()
