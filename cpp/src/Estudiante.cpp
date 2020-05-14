#include "functions.h"
#include "Estudiante.h"

using namespace std;

Estudiante::Estudiante(string input) {
    stringstream ss(input);
    vector<int> posComs = getCommasPosition(input);
    
    if (posComs.size() != 1) throw "CSVFormatException, commas number is different than expected";

    string str_attributes[2]; 
    applySubstrings(posComs, input, str_attributes, sizeof(str_attributes)/sizeof(*str_attributes));

    this->id = removeMarks(str_attributes[0]);
    this->hasImpairment = (str_attributes[1].compare("1")==0)? true : false;
}

Estudiante::operator const char *() {
    ostringstream ss;
    ss << "------INFORMACIÓN DE ESTUDIANTE------" << endl
    << "ID: " << id << endl
    << "Discapacitado: " << (hasImpairment? "true" : "false") << endl
    << "-------------------------------------" << endl;
    ss.str();
    classString = ss.str();
    return classString.c_str();         //Return a pointer
}

Estudiante::~Estudiante() = default;