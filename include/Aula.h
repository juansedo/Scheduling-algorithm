#ifndef AULA_H
#define AULA_H

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


#endif /* AULA_H */