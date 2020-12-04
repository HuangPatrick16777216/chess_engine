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
#include "move.hpp"
using namespace std;


Move::~Move() {

}

Move::Move() {

}

Move::Move(vector<int> sq_start, vector<int> sq_end, string promotion) {
    _square_start = sq_start;
    _square_end = sq_end;
    _promotion = _symbol_to_piece(promotion);
}

vector<int> Move::get_start() {
    return _square_start;
}

vector<int> Move::get_end() {
    return _square_end;
}

int Move::get_promotion() {
    return _promotion;
}

int Move::_symbol_to_piece(string symbol) {
    if (symbol == "") return 0;
    else if (symbol == "P") return 1;
    else if (symbol == "N") return 2;
    else if (symbol == "B") return 3;
    else if (symbol == "R") return 4;
    else if (symbol == "Q") return 5;
    else if (symbol == "K") return 6;
    else if (symbol == "p") return 11;
    else if (symbol == "n") return 12;
    else if (symbol == "b") return 13;
    else if (symbol == "r") return 14;
    else if (symbol == "q") return 15;
    else if (symbol == "k") return 16;
    return 0;
}