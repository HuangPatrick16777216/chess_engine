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

#pragma once
#include <iostream>
#include <vector>
#include <string>
#include "move.hpp"
using namespace std;


class Position {
    /*
    ALL COORDS ARE (row, col)
    0=empty, 1=wp, 2=wn, 3=wb, 4=wr, 5=wq, 6=wk, 11=bp, 12=bn, 13=bb, 14=br, 15=bq, 16=bk
    0 = horizontal, 1 = vertical, 2 = positive slope diagonal, 3 = negative slope diagonal
    */
    public:
        ~Position();
        Position();

        string print();
        void push(Move);
        void push_uci(string);

    private:
        bool _turn;
        vector<vector<int>> _position;

        string _piece_to_symbol(int);

        vector<int> _get_king_pos(bool);
        bool _is_pin(vector<int>, int);
};