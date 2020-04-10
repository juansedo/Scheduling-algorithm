#include "functions.h"
#include "Aula.h"

using namespace std;

Aula::Aula(string input) {
    stringstream ss(input);
    string token;
    
    vector<int> posComs = getCommasPosition(input);
    
    if (posComs.size() != 3) throw "CSVFormatException, commas number is lower than expected";

    string str_type = input.substr(0, posComs[0]);
    string str_classroom = input.substr(posComs[0] + 1, posComs[1] - posComs[0] - 1);
    string str_capacity = input.substr(posComs[1] + 1, posComs[2] - posComs[1] - 1);
    string str_access = input.substr(posComs[2] + 1, 1);

    this->type = removeMarks(str_type);
    this->classroom = removeMarks(str_classroom);
    try {
        this->capacity = stoi(str_capacity);
    }
    catch (...) {
        this->capacity = -1;                //N/A
    }
    this->access = (str_access.compare("0")==0)? false : true;
}

Aula::operator const char *() {
    ostringstream ss;
    ss << "------INFORMACIÓN DE AULA------" << endl
    << "Tipo: " << type << endl
    << "Clase: " << classroom << endl 
    << "Capacidad: " << ((capacity != -1)? to_string(capacity) : "N/A") << endl
    << "Acceso: " << (access? "true" : "false") << endl
    << "-------------------------------" << endl;
    ss.str();
    classString = ss.str();
    return classString.c_str();         //Return a pointer
}

Aula::~Aula() = default;