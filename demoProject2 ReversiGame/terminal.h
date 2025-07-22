//
// Created by ancientmodern on 2022/6/24.
//

#ifndef REVERSI_TERMINAL_H
#define REVERSI_TERMINAL_H

#define MAX_CMD_LENGTH 64

#define RESET   "\033[0m"
#define BLACK   "\033[30m"      /* Black */
#define RED     "\033[31m"      /* Red */
#define GREEN   "\033[32m"      /* Green */
#define YELLOW  "\033[33m"      /* Yellow */
#define BLUE    "\033[34m"      /* Blue */
#define MAGENTA "\033[35m"      /* Magenta */
#define CYAN    "\033[36m"      /* Cyan */
#define WHITE   "\033[37m"      /* White */

void help();

void version();

int loop(Game *game);

void load(Game *game, char *filename);

void save(Game *game, char *filename);

#endif //REVERSI_TERMINAL_H
