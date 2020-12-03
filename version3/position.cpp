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