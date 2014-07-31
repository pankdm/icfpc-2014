all: maze_gen

maze_gen: maze_gen.cpp
	g++ -o maze_gen -O2 -Wall maze_gen.cpp

