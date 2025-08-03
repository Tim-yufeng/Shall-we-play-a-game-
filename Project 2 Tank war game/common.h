#pragma once
#include<iostream>

const int MAX_SIZE=20;
// define direction of tank and movement
 enum Direction {
  D_Left, D_Up, D_Right, D_Down
 };
 enum Move {
  M_Forward, M_Left, M_Right, M_Invalid
 };
 enum GameMode {PVP, PVE, DEMO};

 #define RED     "\033[31m"
#define BLUE    "\033[34m"
#define GREEN   "\033[32m"
#define YELLOW  "\033[33m"
#define CYAN    "\033[36m"
#define PURPLE  "\033[35m"
#define RESET   "\033[0m"
