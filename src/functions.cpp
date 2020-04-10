#include "functions.h"

using namespace std;

vector<int> getCommasPosition(string input) {
    vector<int> posComs;
    bool isComs = false;
    for (int i = 0; i < input.length(); i++) {
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