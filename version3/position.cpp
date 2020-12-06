/*
  A UCI compatible Chess engine.
  Copyright (C) 2020 HuangPatrick16777216

  This program is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  This program is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with this program.  If not, see <https://www.gnu.org/licenses/>.
*/

#include <iostream>
#include <vector>
#include <string>
#include "position.hpp"
#include "move.hpp"
using namespace std;


Position::~Position() {}

Position::Position() {
    _position = {
        {14, 12, 13, 15, 16, 13, 12, 14},
        {11, 11, 11, 11, 11, 11, 11, 11},
        {0,  0,  0,  0,  0,  0,  0,  0},
        {0,  0,  0,  0,  0,  0,  0,  0},
        {0,  0,  0,  0,  0,  0,  0,  0},
        {0,  0,  0,  0,  0,  0,  0,  0},
        {1,  1,  1,  1,  1,  1,  1,  1},
        {4,  2,  3,  5,  6,  3,  2,  4}
    };
    _turn = true;
}

string Position::print() {
    string print_str;
    string line_str, col_str;
    line_str = " +---+---+---+---+---+---+---+---+\n";
    col_str = " | ";

    print_str += line_str;
    for (auto row: _position) {
        for (auto piece: row) {
            print_str += col_str;
            print_str += _piece_to_symbol(piece);
        }
        print_str += col_str;
        print_str += "\n";
        print_str += line_str;
    }
    return print_str;
}

void Position::push(Move move) {
    vector<int> sq_start, sq_end;
    int promo, piece_start, piece_end;

    sq_start = move.get_start();
    sq_end = move.get_end();
    promo = move.get_promotion();

    piece_start = _position[sq_start[0]][sq_start[1]];
    piece_end = _position[sq_end[0]][sq_end[1]];

    if (promo == 0) _position[sq_end[0]][sq_end[1]] = piece_start;
    else {
        if (_turn) _position[sq_end[0]][sq_end[1]] = promo;
        else _position[sq_end[0]][sq_end[1]] = promo + 10;
    }
    _position[sq_start[0]][sq_start[1]] = 0;
    _turn = !_turn;
}

void Position::push_uci(string uci) {
    Move move;
    move.parse_uci(uci);
    push(move);
}

string Position::_piece_to_symbol(int piece) {
    switch (piece) {
        case 0: return " ";
        case 1: return "P";
        case 2: return "N";
        case 3: return "B";
        case 4: return "R";
        case 5: return "Q";
        case 6: return "K";
        case 11: return "p";
        case 12: return "n";
        case 13: return "b";
        case 14: return "r";
        case 15: return "q";
        case 16: return "k";
        default: return " ";
    }
}

vector<int> Position::_get_king_pos(bool color) {
    int piece;
    if (color) piece = 6;
    else piece = 16;

    for (auto row = 0; row < 7; row++) {
        for (auto col = 0; col < 7; col++) {
            if (_position[row][col] == piece) return {row, col};
        }
    }
}

bool Position::_is_pin(vector<int> position, int direction) {
    int piece, grid1, grid2, diag1, diag2;
    vector<int> king_pos;

    piece = _position[position[0]][position[1]];
    if (piece == 0 || piece == 6 || piece == 16) return false;

    if (1 <= piece <= 6) {
        king_pos = _get_king_pos(true);
        grid1 = 15;
        grid2 = 14;
        diag1 = 15;
        diag2 = 13;
    } else {
        king_pos = _get_king_pos(false);
        grid1 = 5;
        grid2 = 4;
        diag1 = 5;
        diag2 = 3;
    }

    if (direction == 0 && position[0] == king_pos[0]) {
        if (king_pos[1] < position[1]) {
            for (auto col = position[1] + 1; col < 8; col++) {
                if (_position[position[0]][col] == grid1) return true;
                else if (_position[position[0]][col] == grid2) return true;
            }
        } else {
            for (auto col = position[1] - 1; col >= 0; col--) {
                if (_position[position[0]][col] == grid1) return true;
                else if (_position[position[0]][col] == grid2) return true;
            }
        }
    } else if (direction == 1 && position[1] == king_pos[1]) {
        if (king_pos[0] < position[0]) {
            for (auto row = position[0] + 1; row < 8; row++) {
                if (_position[row][position[1]] == grid1) return true;
                if (_position[row][position[1]] == grid2) return true;
            }
        }
    }
    
    return false;
}