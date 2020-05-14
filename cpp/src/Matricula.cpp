#include "functions.h"
#include "Matricula.h"

using namespace std;

Matricula::Matricula(string input) {
    stringstream ss(input);
    vector<int> posComs = getCommasPosition(input);
    
    if (posComs.size() != 2) throw "CSVFormatException, commas number is different than expected";

    string str_attributes[3]; 
    applySubstrings(posComs, input, str_attributes, sizeof(str_attributes)/sizeof(*str_attributes));

    this->id_student = str_attributes[0];
    this->id_course = str_attributes[1];
    this->num_group = str_attributes[2];
}

Matricula::operator const char *() {
    ostringstream ss;
    ss << "------INFORMACIÓN DE MATRÍCULA-------" << endl
    << "ID (Estudiante): " << id_student << endl
    << "ID (Curso): " << id_course << endl
    << "Grupo: " << num_group << endl
    << "-------------------------------------" << endl;
    ss.str();
    classString = ss.str();
    return classString.c_str();         //Return a pointer
}

Matricula::~Matricula() = default;