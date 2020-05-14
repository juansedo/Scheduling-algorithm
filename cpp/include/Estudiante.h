#pragma once

class Estudiante {
private:
    std::string classString;
public:
    std::string id;
    bool hasImpairment;
    Estudiante(std::string input);

    operator const char*();
    virtual ~Estudiante();
};