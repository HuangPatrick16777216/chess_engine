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
using namespace std;


string strip(string str) {
    int start, end;
    start = str.find_first_not_of(" ");
    end = str.find_last_not_of(" ");
    return str.substr(start, end-start+1);
}


vector<string> split(string str) {
    // todo debug function
    vector<string> final;
    string curr_char;
    int start;
    bool state=false;  // true if in space

    for (auto i = 0; i < str.size(); i++) {
        curr_char = str.substr(i, 1);

        if (state && curr_char != " ") {
            state = false;
            start = i;
        } else if (!state && curr_char == " ") {
            state = true;
            final.push_back(str.substr(start, i-start));
        }
    }
    final.push_back(str.substr(start, str.size()-start));
    return final;
}