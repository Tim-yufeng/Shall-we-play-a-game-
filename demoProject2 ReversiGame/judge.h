//
// Created by ancientmodern on 2022/6/23.
//

#ifndef REVERSI_JUDGE_H
#define REVERSI_JUDGE_H

#include "global.h"

bool isValidMove(Board board, int x, int y);

void updateBoard(Board board, int x, int y, Disk disk);

Disk curPlayer(int turn);

int judgeEnd(Game *game);

#endif //REVERSI_JUDGE_H
