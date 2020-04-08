objects := main.o
cpp := $(objects:%.o=%.cpp)

EXE := main

all: $(EXE)

$(EXE): $(objects)
		g++ $(objects) -o $(EXE)

$(objects): $(cpp)
		g++ -c $(cpp)

clean:
		rm -rf *.o