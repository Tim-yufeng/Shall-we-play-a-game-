#include<iostream>
#include "Renderer.h"
#include <vector>
#include "map.h"
const char VALID_AREA='.';
const char INVALID_AREA='#';
const char BULLET='*';
const int ORIGIN_SIZE=20;

// two functions for dividing A and B in "showDirection" mode
char convertSymbol(char sym){
    if(sym=='^') return 'U';
    else if(sym=='v') return 'D';
    else if(sym=='<') return 'L';
    else if(sym=='>') return 'R';
    else return '?';
}
char recoverSymbole(char sym){
    if(sym=='U') return '^';
    else if(sym=='D') return 'v';
    else if(sym=='L') return '<';
    else if(sym=='R') return '>';
    else if(sym=='B') return 'B';
    else return '?';
}

void Renderer::render(const Map& map, const Tank& t1, const Tank& t2, const std::vector<Bullet>& bullets, bool showDirection, int turn){
    int size=map.getSize();
    auto [t1_x, t1_y]=t1.getPos();
    auto [t2_x, t2_y]=t2.getPos();
    std::vector<std::vector<char>> grid(ORIGIN_SIZE, std::vector<char>(ORIGIN_SIZE, VALID_AREA));

    for (int i=0; i<ORIGIN_SIZE; i++){
        for(int j=0; j<ORIGIN_SIZE; j++){
            if(i<(ORIGIN_SIZE-size)/2 || i>(size+ORIGIN_SIZE)/2-1 || j<(ORIGIN_SIZE-size)/2 || j>(size+ORIGIN_SIZE)/2-1){    // shrink part
                grid[i][j]=INVALID_AREA;
            }
        }
    }

    // Insert bullets
    int num=0;
    for (const Bullet& b : bullets) {
        num++;
        if (b.canExplode) {
            auto [x, y] = b.getPos();
            if (x >= 0 && x < ORIGIN_SIZE && y >= 0 && y < ORIGIN_SIZE)
                grid[y][x] = BULLET;
        }
    }
    // Insert two tanks
        auto [x1, y1] = t1.getPos();
        if (x1 >= 0 && x1 < ORIGIN_SIZE && y1 >= 0 && y1 < ORIGIN_SIZE){
            if(showDirection) grid[y1][x1] = t1.getSymbol();
            else grid[y1][x1] = t1.getLabel();
        }

        auto [x2, y2] = t2.getPos();
        if (x2 >= 0 && x2 < ORIGIN_SIZE && y2 >= 0 && y2 < ORIGIN_SIZE){
            if(showDirection) grid[y2][x2] = convertSymbol(t2.getSymbol());
            else grid[y2][x2] = t2.getLabel();
        }
        // print map, tank and bullets
    std::cout <<YELLOW<< "Map (size: " << size << "x" << size << "):\n"<<RESET;
    for (int y = 0; y < ORIGIN_SIZE; y++) {
        for (int x = 0; x < ORIGIN_SIZE; x++) {
            if(grid[y][x]=='A'||grid[y][x]=='^'||grid[y][x]=='v'||grid[y][x]=='<'||grid[y][x]=='>') std::cout<<RED<<grid[y][x]<<RESET<<' ';   // paint color to A and B
            else if(grid[y][x]=='B'||grid[y][x]=='U'||grid[y][x]=='D'||grid[y][x]=='L'||grid[y][x]=='R') std::cout<<BLUE<<recoverSymbole(grid[y][x])<<RESET<<' ';
            else if(grid[y][x]=='*') std::cout<<PURPLE<<grid[y][x]<<RESET<<' ';
            else std::cout<<grid[y][x]<<' ';
        }
        std::cout<<std::endl;
    }
    // print information about current turn
    std::cout <<YELLOW<<"Turn: "<<turn<<std::endl<<RESET;
    std::cout <<GREEN<< "Tank " << t1.getLabel() << " Life: " << t1.getLifePt() <<RESET << " | " << CYAN << "Pos: (" << t1_x << "," << t1_y << ")"<<std::endl<<RESET;
    std::cout <<GREEN<< "Tank " << t2.getLabel() << " Life: " << t2.getLifePt() <<RESET << " | " << CYAN << "Pos: (" << t2_x << "," << t2_y << ")"<<std::endl<<RESET;
    std::cout <<YELLOW<< "Fire CD: " << t1.getFireCD()<<"  "<<RESET;
    if(t1.getFireCD()==0) std::cout<<"\033[1;31m"<<"Fire next turn!"<<RESET;
    std::cout<< std::endl;
    std::cout <<YELLOW<< "-------------------------------------------"<<std::endl<<RESET;
}