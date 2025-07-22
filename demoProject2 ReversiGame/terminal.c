//
// Created by ancientmodern on 2022/6/24.
//

#include <stdio.h>
#include <string.h>
#include "global.h"
#include "board.h"
#include "terminal.h"
#include "judge.h"

const char VERSION[] = "0.0.1";

/**
 * @brief Print the help message
 */
void help() {
    // TODO: Implement this function.
    printf("\n");
    printf("Usage: ./reversi [OPTIONS]\n");
    printf("\n");
    printf("A local multiplayer Reversi game.\n");
    printf("\n");
    printf("Options:\n");
    printf("-h|--help Print this help message\n");
    printf("-v|--version Print version information\n");
    printf("\n");
    printf("Commands:\n");
    printf(" AUTO    Automatically process the game by always placing the first valid disk\n");
    printf(" DONE    Manually exit the game\n");
    printf("LOAD filename   Load the game status from the specified file,\n");
    printf("    e.g. LOAD sample.txt If the filename does not exist, sample.txt will be loaded by defaul\n");
    printf("PLACE   x y Place a new disk at position (x, y), e.g. PLACE 3 c\n");
    printf("PRINT   Print current board\n");
    printf("SAVE filename   Save the game status to the specified file, \n");
    printf("    e.g. SAVE sample.txt If the filename does not exist, it will be automatically created\n");
}

/**
 * @brief Print the version information
 */
void version() {
    // TODO: Implement this function.
    printf("Reversi version %s", VERSION);
}

/**
 * @brief Each iteration of the main loop of the command-line interface, reading and processing commands
 * @param game pointer to current game status
 * @return 0 if you want the main program to continue running; return any other value if you want to exit
 */
int loop(Game *game) {
    printBoardColor(game->board);
    if (curPlayer(game->turn) == Black) {
        printf(MAGENTA "Now it's Black's turn.\n" RESET);
    } else {
        printf(CYAN "Now it's White's turn.\n" RESET);
    }
    printf(">> ");
    // TODO: Implement this function.
    char command[MAX_CMD_LENGTH]={0};
    fgets(command,MAX_CMD_LENGTH,stdin);
    if(strlen(command)<=1){
        // only input "\n", continue
        return 0;
    }
    command[strlen(command)-1] = '\0';
    char *token = strtok(command," ");
    while(token!=NULL){
        if(strcmp(token,"DONE")==0){
            printf("Exit Reversi. See you!\n");
            return -1;
        }
        else if(strcmp(token,"AUTO")==0){
            findFirstNext(game->board,command);
        }
        else if(strcmp(token,"SAVE")==0){
            char *filename = strtok(NULL," ");
            save(game,filename);
        }
        else if(strcmp(token,"LOAD")==0){
            char *filename = strtok(NULL," ");
            load(game,filename);
        }
        else if(strcmp(token,"PRINT")==0){
            printBoard(game->board);
        }
        else if(strcmp(token,"PRINTC")==0){
            printBoardColor(game->board);
        }
        else if(strcmp(token,"PLACE")==0){
            //take out the int value of x and y
            char* take_x = strtok(NULL," ");
            char* take_y = strtok(NULL," ");
            int x = (take_x != NULL)?take_x[0]-'1':-1;
            int y = (take_y != NULL)?take_y[0]-'a':-1;
            Disk disk = curPlayer(game->turn);
            if(!isValidMove(game->board,x,y)){
                //input a illegal value
                printf("Invalid, place %d %d! "
                       "Please place your disk again.\n",x,y);
                return 0;
            }
            updateBoard(game->board,x,y,disk);
            // printBoard(game->board);
            // printBoardColor(game->board);
            game->turn++;
            return judgeEnd(game);
        }
         else{
            printf("Unknown command. Ignore it.\n");
            return 0;
        }
        token = strtok(NULL," ");
    }
    return 0;
}

/**
 * @brief Load current game status (board and turn) from a specified file.
 *        Sample file format (see sample.txt):
 *        0 0 0 0 0 0 0 0
 *        0 0 0 0 0 0 0 0
 *        0 0 0 3 0 0 0 0
 *        0 0 3 2 1 0 0 0
 *        0 0 0 1 2 3 0 0
 *        0 0 0 0 3 0 0 0
 *        0 0 0 0 0 0 0 0
 *        0 0 0 0 0 0 0 0
 *        Turn == 0
 * @file sample.txt
 * @param game pointer to current game status
 * @param filename input filename
 */
void load(Game *game, char *filename) {
    FILE *fp = fopen(filename, "r");
    if (fp == NULL) {
        fp = fopen("sample.txt", "r");
        printf(RED "%s does not exist, load sample.txt by default.\n" RESET, filename);
    }
    // TODO: Implement this function.
    for(int i=0; i<BOARD_SIZE; i++){
        for(int j=0; j<BOARD_SIZE; j++){
            int disk;
            fscanf(fp, "%d", &disk);
            game->board[i][j]=disk;
        }
    }
    fscanf(fp, "Turn==%d\n", &(game->turn));
    fclose(fp);
}

/**
 * @brief Save current game status (board and turn) to a specified file.
 *        Sample file format (see sample.txt):
 *        0 0 0 0 0 0 0 0
 *        0 0 0 0 0 0 0 0
 *        0 0 0 3 0 0 0 0
 *        0 0 3 2 1 0 0 0
 *        0 0 0 1 2 3 0 0
 *        0 0 0 0 3 0 0 0
 *        0 0 0 0 0 0 0 0
 *        0 0 0 0 0 0 0 0
 *        Turn == 0
 * @file sample.txt
 * @param game pointer to current game status
 * @param filename output filename
 */
void save(Game *game, char *filename) {
    // TODO: Implement this function.
    FILE *fp = fopen(filename, "w");
    if (fp == NULL) {
        fp = fopen("sample.txt", "w");
        printf(RED "%s does not exist, load sample.txt by default.\n" RESET, filename);
    }
    for(int i=0; i<BOARD_SIZE; i++){
        for(int j=0; j<BOARD_SIZE; j++){
            int disk=game->board[i][j];
            fprintf(fp, "%d", disk);
        }
        fprintf(fp, "\n");
    }
    fprintf(fp, "Turn==%d\n", game->turn);
    fclose(fp);

}
