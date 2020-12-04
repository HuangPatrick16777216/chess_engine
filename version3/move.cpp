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

void Move::parse_uci(string uci) {
    string sq1=uci.substr(0, 2), sq2=uci.substr(2, 2);
    int promotion;

    _square_start = _square_to_coords(sq1);
    _square_end = _square_to_coords(sq2);

    if (uci.size() > 4) {
        promotion = _symbol_to_piece(uci.substr(4, 1));
        if (promotion >= 10) promotion -= 10;
        _promotion = promotion;
    } else {
        _promotion = 0;
    }
}

void Move::set_start(vector<int> square) {
    _square_start = square;
}

void Move::set_end(vector<int> square) {
    _square_end = square;
}

void Move::set_promotion(int promotion) {
    _promotion = promotion;
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

string Move::_coords_to_square(vector<int> coords) {
    int c1=coords[0], c2=coords[1];
    string square="";

    if (c2 == 0) square += "a";
    else if (c2 == 1) square += "b";
    else if (c2 == 2) square += "c";
    else if (c2 == 3) square += "d";
    else if (c2 == 4) square += "e";
    else if (c2 == 5) square += "f";
    else if (c2 == 6) square += "g";
    else if (c2 == 7) square += "h";

    if (c1 == 0) square += "8";
    else if (c1 == 1) square += "7";
    else if (c1 == 2) square += "6";
    else if (c1 == 3) square += "5";
    else if (c1 == 4) square += "4";
    else if (c1 == 5) square += "3";
    else if (c1 == 6) square += "2";
    else if (c1 == 7) square += "1";

    return square;
}

vector<int> Move::_square_to_coords(string square) {
    string ch1=square.substr(0, 1), ch2=square.substr(1, 1);
    vector<int> coords;

    if (ch2 == "1") coords.push_back(7);
    else if (ch2 == "2") coords.push_back(6);
    else if (ch2 == "3") coords.push_back(5);
    else if (ch2 == "4") coords.push_back(4);
    else if (ch2 == "5") coords.push_back(3);
    else if (ch2 == "6") coords.push_back(2);
    else if (ch2 == "7") coords.push_back(1);
    else if (ch2 == "8") coords.push_back(0);

    if (ch1 == "a") coords.push_back(0);
    else if (ch1 == "b") coords.push_back(1);
    else if (ch1 == "c") coords.push_back(2);
    else if (ch1 == "d") coords.push_back(3);
    else if (ch1 == "e") coords.push_back(4);
    else if (ch1 == "f") coords.push_back(5);
    else if (ch1 == "g") coords.push_back(6);
    else if (ch1 == "h") coords.push_back(7);

    return coords;
}