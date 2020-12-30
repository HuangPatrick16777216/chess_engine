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
#include "funcs.hpp"
#include "position.hpp"
using namespace std;


int main() {
    string msg;
    Position position;

    while (true) {
        getline(cin, msg);
        msg = strip(msg);

        if (msg == "quit") return 0;
        else if (msg == "isready") cout << "readyok" << endl;
        else if (msg == "uci") cout << "uciok" << endl;
        else if (msg == "d") cout << position.print() << endl;
    }
}