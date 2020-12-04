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
using namespace std;


class Move {
    public:
        ~Move();
        Move();
        Move(vector<int>, vector<int>, string="");

        vector<int> get_start();
        vector<int> get_end();
        int get_promotion();

        void parse_uci(string);
        void set_start(vector<int>);
        void set_end(vector<int>);
        void set_promotion(int);

    private:
        vector<int> _square_start;
        vector<int> _square_end;
        int _promotion;

        int _symbol_to_piece(string);
        string _coords_to_square(vector<int>);
        vector<int> _square_to_coords(string);
};