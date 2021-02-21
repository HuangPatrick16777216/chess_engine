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

import chess


def evaluate(board: chess.Board):
    # Material
    material = 0
    material += len(board.pieces(chess.PAWN, chess.WHITE))
    material += 3 * len(board.pieces(chess.KNIGHT, chess.WHITE))
    material += 3 * len(board.pieces(chess.BISHOP, chess.WHITE))
    material += 5 * len(board.pieces(chess.ROOK, chess.WHITE))
    material += 9 * len(board.pieces(chess.QUEEN, chess.WHITE))
    material -= len(board.pieces(chess.PAWN, chess.BLACK))
    material -= 3 * len(board.pieces(chess.KNIGHT, chess.BLACK))
    material -= 3 * len(board.pieces(chess.BISHOP, chess.BLACK))
    material -= 5 * len(board.pieces(chess.ROOK, chess.BLACK))
    material -= 9 * len(board.pieces(chess.QUEEN, chess.BLACK))

    return material
