#pragma once

class Distancia {
private:
    std::string classString;
public:
    std::string initial_block;
    std::string final_block;
    int distance;

    Distancia(std::string input);

    operator const char*();
    virtual ~Distancia();
};