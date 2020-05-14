#pragma once
#include "libraries.h"

std::vector<int> getCommasPosition(std::string input);
std::string removeMarks(std::string str);
std::string substring(std::string input, int init_pos, int end_pos = -1);
void applySubstrings(std::vector<int> posComs, std::string input, std::string* arr, int arr_length);