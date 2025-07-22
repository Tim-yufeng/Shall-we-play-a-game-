//
// Created by ancientmodern on 2022/6/23.
//

#include "judge.h"
#include "board.h"

/**
 * @param board pointer to the board
 * @param x horizontal axis (row), should be 0 ~ BOARD_SIZE if in the board
 * @param y vertical axis (column), should be 0 ~ BOARD_SIZE if in the board
 * @return true if placing a disk on (x, y) is valid
 */
bool isValidMove(Board board, int x, int y) {
     return ((isinBoard(x, y)) && (board[x][y] == Next));
}

/**
 * @brief Update the board after the disk is put in spot (x,y)
 * 
 * @param board pointer to the board
 * @param x horizontal axis (row), should be 0 ~ BOARD_SIZE if in the board
 * @param y vertical axis (column), should be 0 ~ BOARD_SIZE if in the board
 * @param disk the disk type to be placed
 * @call: probe()
 */
void updateBoard(Board board, int x, int y, Disk disk) {
    int oppos[BOARD_SIZE * BOARD_SIZE] = {0};
    int len = probe(board, x, y, disk, oppos);
    for (int i = 0; i < len; ++i) {
        board[oppos[i] / BOARD_SIZE][oppos[i] % BOARD_SIZE] = disk;
    }
    board[x][y] = disk;
}

/**
 * @brief Return the disk type in the current turn
 * 
 * @param turn Tue current turn
 * @hint Think about the integer value of enum
 */
Disk curPlayer(int turn) {
    return turn % 2 + 1;
}

/**
 * @brief judge whether the game comes to end
 * @printf winning message
 * @param game Pointer to the game struct
 * @return 0 means continue, 1 means black win, 2 means white win, 3 means draw
 */
int judgeEnd(Game *game) {
    if (showNext(game->board, curPlayer(game->turn)) || showNext(game->board, curPlayer(++(game->turn)))) {
        return 0;
    }
    int blackCnt = countBoard(game->board, Black);
    int whiteCnt = countBoard(game->board, White);
    if (blackCnt > whiteCnt) {
        printf("Black Wins! See you.\n");
        printBoardColor(game->board);
        return 1;
    } else if (blackCnt < whiteCnt) {
        printf("White Wins! See you.\n");
        printBoardColor(game->board);
        return 2;
    } else {
        printf("Draw! Good Game.\n");
        printBoardColor(game->board);
        return 3;
    }
}
