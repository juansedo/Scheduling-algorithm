#include "libraries.h"
#include "Aula.h"

using namespace std;

Aula::Aula(string input)
{
    stringstream ss(input);
    string token;
    
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
    this->type = input.substr(0,posComs[0]);
    this->classroom = input.substr(posComs[0] + 1, posComs[1] - posComs[0] - 1);
    this->capacity = stoi(input.substr(posComs[1] + 1, posComs[2] - posComs[1] - 1));
    this->access = (input.substr(posComs[2] + 1).compare("1")==0)? true : false;
    
    // int i = 0;
    // while (getline(ss, token, ',')) {
    //     switch (i)
    //     {
    //     case 0:
    //         this->type = token;
    //         break;
    //     case 1:
    //         this->classroom = token;
    //         break;
    //     case 2:
    //         this->capacity = stoi(token);
    //         break;
    //     case 3:
    //         this->access = (token.compare("1") == 1) ? true : false;
    //         break;
    //     default:
    //         break;
    //     }
    //     i++;
    // }
}

Aula::operator const char *() {
    ostringstream ss;
    ss << "----INFORMACIÓN DE AULA----" << endl
    << "Tipo: " << type << endl
    << "Clase: " << classroom << endl 
    << "Capacidad: " << capacity << endl
    << "Acceso: " << (access? "true" : "false");
    
    ss.str();

    classString = ss.str();
    return classString.c_str();         //Return a pointer
}

Aula::~Aula() = default;