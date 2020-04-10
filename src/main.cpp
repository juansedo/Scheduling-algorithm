#include "libraries.h"
#include "Aula.h"

using namespace std;

template <class T>
vector<T> separateDataset(string filename) {
  ifstream file(filename);
  string line;
  vector<T> data;
  if (file.is_open()) {
    while (getline(file, line)) {
      cout << line << endl;
      T t(line);
      data.push_back(t);
      cout << data[data.size() - 1] << endl;
    }
    cout << "Archivo casi cerrado" << endl;
    file.close();
    cout << "Archivo cerrado" << endl;
  }
  else {
    cout << "Error de lectura" << endl;
  }
  return data;
}

int main() {
  //Aula a("7108,Aula de clase,28,1");
  vector<Aula> aulaDataset = separateDataset<Aula>("./src/datasets/aulas.csv");
  cout << "Programa" << endl;
  cout << aulaDataset.size() << endl;
  cout << aulaDataset[1] << endl;
  
  return 0;
}
