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