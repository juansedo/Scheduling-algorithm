#include "libraries.h"
#include "Aula.h"
#include "Estudiante.h"
#include "Matricula.h"
#include "Distancia.h"

using namespace std;

template <class T>
vector<T> separateDataset(string filename) {
  ifstream file("./bin/datasets/" + filename);
  string line;
  vector<T> data;
  
  if (file.is_open()) {
    int lineCounter = 1;
    while (getline(file, line)) {
      try {
        T t(line);
        data.push_back(t);
        lineCounter++;
        cout << t << endl;
      }
      catch(const char* exp) {
        cout << "[" << lineCounter << "]:" << exp << endl;
      }
    }
    file.close();
  }
  else cout << "Error de lectura: " << filename << endl;
  return data;
}

int main() {
  //vector<Aula> aulaDataset = separateDataset<Aula>("aulas.csv");
  //cout << aulaDataset.size() << endl;
  //cout << aulaDataset[1] << endl;
  
  //vector<Estudiante> estudianteDataset = separateDataset<Estudiante>("estudiantes.csv");
  //cout << estudianteDataset.size() << endl;
  //cout << estudianteDataset[1] << endl;

  //vector<Matricula> matriculaDataset = separateDataset<Matricula>("mat20192.csv");

  vector<Distancia> distanciaDataset = separateDataset<Distancia>("DistanciasBloques.csv");
  cout << distanciaDataset.size() << endl;
  cout << distanciaDataset[1] << endl;
  return 0;
}
