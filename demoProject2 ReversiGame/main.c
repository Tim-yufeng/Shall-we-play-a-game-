#include "global.h"
#include "board.h"
#include "terminal.h"
#include <string.h>

int main(int argc, char *argv[]) {
    if(argc>2){
        printf("Too many arguments!\n");
    }
    else if(argc==2){

    if(strcmp(argv[1],"-v")==0){
        version();     
    }
    else if(strcmp(argv[1], "-h")==0){
        help();
    }
    else{
        printf("Unknown argument!\n");
    }
    }
    if(argc==1){
        Game game;
        printf("Game start!\n");
        game.turn=0;
        initBoard(game.board);
        showNext(game.board, Black);
        while (loop(&game)==0);
        return 0;
        
    }
    // TODO: Implement this function
    return 0;
}

