//
// Created by ancientmodern on 2022/6/21.
//

#include "board.h"
#include "terminal.h"
#include <stdio.h>

const char icons[4] = {' ', 'X', 'O', '`'};
const int dx[8] = {1, 1, 0, -1, -1, -1, 0, 1};
const int dy[8] = {0, 1, 1, 1, 0, -1, -1, -1};

/**
 * @brief Initialize the game board, all the spot should be Blank except the four in the center
 *
 * @param board pointer to the board
 */
void initBoard(Board board) {
    for (int i = 0; i < BOARD_SIZE; ++i) {
        for (int j = 0; j < BOARD_SIZE; ++j) {
            board[i][j] = Blank;
        }
    }
    board[3][3] = board[4][4] = White;
    board[3][4] = board[4][3] = Black;
}

/**
 * @param disk the disk type, see Disk
 * @return true if the disk is not Black or White, false otherwise
 */
bool isBlank(Disk disk) {
    return !(disk == Black || disk == White);
}

/**
 * @param x horizontal axis (row), should be 0 ~ BOARD_SIZE if in the board
 * @param y vertical axis (column), should be 0 ~ BOARD_SIZE if in the board
 * @return true if the position is in the board, false otherwise
 */
bool isinBoard(int x, int y) {
    return (0 <= x && x < BOARD_SIZE && 0 <= y && y < BOARD_SIZE);
}

/**
 * @param disk1 the first disk type
 * @param disk2 the second disk type
 * @return true if the two disk are opposite to each other, namely one Black one White
 */
bool isoppo(Disk disk1, Disk disk2) {
    return (disk1 == Black && disk2 == White) || (disk1 == White && disk2 == Black);
}

/**
 * @brief Assuming we place a specified disk on the given position,
 *        calculate the number and positions of disks that will be reversed
 * 
 * @param board 
 * @param x horizontal axis (row), should be 0 ~ BOARD_SIZE if in the board
 * @param y vertical axis (row)), should be 0 ~ BOARD_SIZE if in the board
 * @param disk the disk type to be placed
 * @param oppos an array storing the positions of disks that will be reversed, which is updated in the function
 *              indexing rule: index == BOARD_SIZE * x + y
 * @return the number of disks that will be reversed
 */
int probe(Board board, int x, int y, Disk disk, int oppos[BOARD_SIZE * BOARD_SIZE]) {
    int oppoCount = 0;
    for (int dir = 0; dir < 8; dir++) {
        int curX = x + dx[dir];
        int curY = y + dy[dir];
        int prevOppoCount = oppoCount;
        if (!isinBoard(curX, curY) || isBlank(board[curX][curY])) continue;
        while (isinBoard(curX, curY) && isoppo(board[curX][curY], disk)) {
            oppos[oppoCount++] = curX * 8 + curY;
            curX += dx[dir];
            curY += dy[dir];
        }
        if (!((oppoCount > prevOppoCount) && isinBoard(curX, curY) && !isBlank(board[curX][curY]))) {
            oppoCount = prevOppoCount;
        }
    }
    return oppoCount;
}

/**
 * @brief Update the board, mark all the non-Blank spot with Next if the disk could be placed in the next turn, otherwise leave it Blank
 *
 * @param board pointer to the board
 * @param disk the disk type to be placed, Black or White
 * @return true if there is a spot that the disk could be placed in the next turn
 * @call function probe()
 */
bool showNext(Board board, Disk disk) {
    bool flag = false;
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            int oppos[64] = {0};
            if (isBlank(board[i][j])) {
                if (probe(board, i, j, disk, oppos) > 0) {
                    flag = true;
                    board[i][j] = Next;
                } else {
                    board[i][j] = Blank;
                }
            }
        }
    }
    return flag;
}

/**
 * @brief Count the number of chess of the given type of disk
 * 
 * @param board pointer to the board
 * @param disk disk type to be counted
 * @return number of disks having the same type as the input disk
 */
int countBoard(Board board, Disk disk) {
    int cnt = 0;
    for (int i = 0; i < BOARD_SIZE; ++i) {
        for (int j = 0; j < BOARD_SIZE; ++j) {
            cnt += (board[i][j] == disk);
        }
    } 
    return cnt;
}

/**
 * @brief Find the first spot that is "Next" in row-major priority
 * 
 * @param board pointer to the board
 * @param buffer pointer to the buffer, output is stored here
 * @output e.g. PLACE 3 d (stored in buffer)
 * @return 1 if a spot with "Next" is found, 0 otherwise
 * @hint Use sprintf()
 */
int findFirstNext(Board board, char *buffer) {
    for (int i = 0; i < BOARD_SIZE; i++) {
        for (int j = 0; j < BOARD_SIZE; j++) {
            if (board[i][j] == Next) {
                sprintf(buffer, "       PLACE %d %c\n", i + 1, j + 97);
                printf("%s", buffer);
                return 1;
            }
        }
    }
    sprintf(buffer, "      PRINTC\n");
    return 0;
}

/**
 * @brief Print the board
 * 
 * @param board pointer to the board
 */
void printBoard(Board board) {
    printf("   a   b   c   d   e   f   g   h\n");
    for (int i = 0; i < BOARD_SIZE; ++i) {
        printf(" +---+---+---+---+---+---+---+---+\n");
        printf("%d|", i + 1);
        for (int j = 0; j < BOARD_SIZE; ++j) {
            printf(" %c |", icons[board[i][j]]);
        }
        printf("\n");
    }
    printf(" +---+---+---+---+---+---+---+---+\n");
    printf("Black (X) Counts: %d\n", countBoard(board, Black));
    printf("White (O) Counts: %d\n", countBoard(board, White));
    printf("====================================\n");
}

/**
 * @brief Print the board with color
 * 
 * @param board pointer to the board
 */
void printBoardColor(Board board) {
    printf("   a   b   c   d   e   f   g   h\n");
    for (int i = 0; i < BOARD_SIZE; ++i) {
        printf(" +---+---+---+---+---+---+---+---+\n");
        printf("%d|", i + 1);
        for (int j = 0; j < BOARD_SIZE; ++j) {
            if (board[i][j] == Black) {
                printf(MAGENTA " X " RESET "|");
            } else if (board[i][j] == White) {
                printf(CYAN " O " RESET "|");
            } else if (board[i][j] == Next) {
                printf(GREEN " ` " RESET "|");
            } else {
                printf("   |");
            }
        }
        printf("\n");
    }
    printf(" +---+---+---+---+---+---+---+---+\n");
    printf(MAGENTA "Black (X) Counts: %d\n" RESET, countBoard(board, Black));
    printf(CYAN "White (O) Counts: %d\n" RESET, countBoard(board, White));
    printf("====================================\n");
}

