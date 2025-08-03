# Makefile for Tank Game

CXX = g++
CXXFLAGS = -std=c++17 -Wall -g

SRCS = AI.cpp bullet.cpp game.cpp main.cpp map.cpp Renderer.cpp tank.cpp
OBJS = $(SRCS:.cpp=.o)

TARGET = main

all: $(TARGET)

$(TARGET): $(OBJS)
	$(CXX) $(CXXFLAGS) -o $@ $(OBJS)

%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

clean:
	rm -f *.o $(TARGET)
