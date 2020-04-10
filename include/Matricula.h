#pragma once

class Matricula {
private:
    std::string classString;
public:
    std::string id_student;
    std::string id_course;
    std::string num_group;

    Matricula(std::string input);

    operator const char*();
    virtual ~Matricula();
};