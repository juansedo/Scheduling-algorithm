#pragma once

class Aula {
private:
    std::string classString;
public:
    std::string type;
    std::string classroom;
    int capacity;
    bool access;

    Aula(std::string input);
    operator const char* ();
    virtual ~Aula();
};