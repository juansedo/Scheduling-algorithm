#include "functions.h"
#include "Aula.h"

using namespace std;

Aula::Aula(string input) {
    stringstream ss(input);
    vector<int> posComs = getCommasPosition(input);
    
    if (posComs.size() != 3) throw "CSVFormatException, commas number is different than expected";

    string str_attributes[4]; 
    applySubstrings(posComs, input, str_attributes, sizeof(str_attributes)/sizeof(*str_attributes));

    this->type = removeMarks(str_attributes[0]);
    this->classroom = removeMarks(str_attributes[1]);
    try {
        this->capacity = stoi(str_attributes[2]);
    }
    catch (...) {
        this->capacity = -1;                //N/A
    }
    this->access = (str_attributes[3].compare("1")==0)? true : false;
}

Aula::operator const char *() {
    ostringstream ss;
    ss << "---------INFORMACIÓN DE AULA---------" << endl
    << "Tipo: " << type << endl
    << "Clase: " << classroom << endl 
    << "Capacidad: " << ((capacity != -1)? to_string(capacity) : "N/A") << endl
    << "Acceso: " << (access? "true" : "false") << endl
    << "-------------------------------------" << endl;
    ss.str();
    classString = ss.str();
    return classString.c_str();         //Return a pointer
}

Aula::~Aula() = default;