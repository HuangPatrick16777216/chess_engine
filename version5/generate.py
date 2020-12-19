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
import pickle
import time
import random
import chess
import chess.engine

engine_path = "/home/patrick/work/chess/engines/stockfish12"
depth = 12
total = 1000

final = []
engine = chess.engine.SimpleEngine.popen_uci(engine_path)
time_start = time.time()

sys.stdout.write("Analyzing position ")
sys.stdout.flush()
for i in range(total):
    time_elapse = time.time() - time_start
    elapse_msg = str(int(time_elapse*100)/100)
    remain_msg = str(int(time_elapse/(i+1)*(total-i)*100)/100)
    msg = f"{i+1} of {total}; {elapse_msg}{' ' * (7-len(elapse_msg))} elapsed; {remain_msg}{' ' * (7-len(remain_msg))} remaining"
    sys.stdout.write(msg)
    sys.stdout.flush()
    sys.stdout.write("\b" * len(msg))
    sys.stdout.write(" " * len(msg))
    sys.stdout.write("\b" * len(msg))

    num_moves = random.randint(1, 100)
    board = chess.Board()
    for j in range(num_moves):
        legal_moves = list(board.generate_legal_moves())
        if len(legal_moves) == 0:
            break
        board.push(random.choice(legal_moves))

    evaluation = engine.analyse(board, chess.engine.Limit(depth=depth))["score"].pov(chess.WHITE)
    final.append((board.fen(), evaluation))

sys.stdout.write(f"finished in {int((time.time()-time_start) * 100) / 100} seconds.")
sys.stdout.flush()

#for i in final: print(i)