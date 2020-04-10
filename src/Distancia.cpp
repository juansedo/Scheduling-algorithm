#include "functions.h"
#include "Distancia.h"

using namespace std;

Distancia::Distancia(string input) {
    stringstream ss(input);
    vector<int> posComs = getCommasPosition(input);
    
    if (posComs.size() != 2) throw "CSVFormatException, commas number is different than expected";

    string str_attributes[3]; 
    applySubstrings(posComs, input, str_attributes, sizeof(str_attributes)/sizeof(*str_attributes));

    this->initial_block = str_attributes[0];
    this->final_block = str_attributes[1];
    try {
        this->distance = stoi(str_attributes[2]);
    }
    catch (...) {
        this->distance = -1;                //N/A
    }
}

Distancia::operator const char *() {
    ostringstream ss;
    ss << "------INFORMACIÓN DE DISTANCIA-------" << endl
    << initial_block << " -> " << final_block << endl
    << "Distancia: " << ((distance != -1)? to_string(distance) : "N/A") << endl
    << "-------------------------------------" << endl;
    ss.str();
    classString = ss.str();
    return classString.c_str();         //Return a pointer
}

Distancia::~Distancia() = default;