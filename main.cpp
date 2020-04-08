#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <vector>

using namespace std;

void separateDataset(string filename, int cols);

class Aula {
public:
  string classroom;
  int type;
  int capacity;
  bool access;

  Aula(string input) {
    stringstream ss(input);
    string token;
    int i = 0;
    while(getline(ss, token, ',')) {
      switch(i++) {
        case 0:
          type = stoi(token);
          break;
        case 1:
          classroom = token;
          break;
        case 2:
          capacity = stoi(token);
          break;
        case 3:
          access = (token.compare("1") == 1)? true: false;
          break;
        default: break;
      }
    }
  }
};


int main(){
  Aula a("7108,Aula de clase,28,1");
  cout << a.classroom << endl;
  cout << a.type << endl;
  cout << a.capacity << endl;
  cout << a.access << endl;
  //separateDataset("./datasets/aulas.csv", 4);
  return 0;
}

template <class T>
void separateDataset(string filename, int cols) {
  fstream file("./datasets/aulas.csv", ios::in);
  string line;
  while(getline(file, line)) {
    vector<T> data(cols);
  }
  file.close();
}