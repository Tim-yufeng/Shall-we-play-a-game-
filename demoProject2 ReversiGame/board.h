//
// Created by ancientmodern on 2022/6/21.
//

#ifndef REVERSI_BOARD_H
#define REVERSI_BOARD_H

#include "global.h"

extern const char icons[4];
extern const int dx[8];
extern const int dy[8];


void initBoard(Board board);

int countBoard(Board board, Disk disk);

void printBoard(Board board);

void printBoardColor(Board board);

bool isBlank(Disk disk);

bool isoppo(Disk disk1, Disk disk2);

int probe(Board board, int x, int y, Disk disk, int oppos[64]);

bool showNext(Board board, Disk disk);

int findFirstNext(Board board,char* buffer);
#endif //REVERSI_BOARD_H

