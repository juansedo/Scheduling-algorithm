#include "functions.h"

using namespace std;

vector<int> getCommasPosition(string input) {
    vector<int> posComs;
    bool isComs = false;
    for (unsigned int i = 0; i < input.length(); i++) {
        switch(input.at(i)) {
            case ',':
                if(!isComs) posComs.push_back(i);
                break;
            case '"':
                isComs = !isComs;
                break;
            default:
                break;
        }
    }
    return posComs;
}

string removeMarks(string str) {
    if (!str.empty() && str.size() > 1 && str.at(0) == '"') {
        str = str.substr(1, str.size() - 2);
    }
    return str;
}

//Return a substring of input in range [init_pos, end_pos)
string substring(string input, int init_pos, int end_pos) {
    if (end_pos == -1) end_pos = input.length() - 1;
    return input.substr(init_pos, end_pos - init_pos);
}

void applySubstrings(vector<int> posComs, string input, string* arr, int arr_length) {
    posComs.push_back(input.length() - 1);
    *(arr) = substring(input, 0, posComs[0]);
    for (int i = 1; i < arr_length; i++) {
        *(arr + i) = substring(input, posComs[i-1] + 1, posComs[i]);
    }
}