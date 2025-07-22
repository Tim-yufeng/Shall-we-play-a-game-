//
// Created by ancientmodern on 2022/6/21.
//

#ifndef REVERSI_GLOBAL_H
#define REVERSI_GLOBAL_H

#include <stdio.h>
#include <stdbool.h>

#define BOARD_SIZE 8

typedef enum {
    Blank, Black, White, Next
} Disk;

typedef Disk Board[BOARD_SIZE][BOARD_SIZE];

typedef struct game {
    Board board;
    int turn;
} Game;

bool isinBoard(int x, int y);

#endif //REVERSI_GLOBAL_H
