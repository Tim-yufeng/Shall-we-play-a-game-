#include<iostream>
#include "Renderer.h"
#include <vector>
#include "map.h"
const char VALID_AREA='.';
const char INVALID_AREA='#';
const char BULLET='*';
const int ORIGIN_SIZE=20;


void Renderer::render(const Map& map, const Tank& t1, const Tank& t2, const std::vector<Bullet>& bullets, bool showDirection, int turn){
    int size=map.getSize();
    // int t1_x, t1_y, t2_x, t2_y;
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

    // Print bullets
    int num=0;
    for (const Bullet& b : bullets) {
        num++;
        if (b.canExplode) {
            auto [x, y] = b.getPos();
            if (x >= 0 && x < ORIGIN_SIZE && y >= 0 && y < ORIGIN_SIZE)
                grid[y][x] = BULLET;
    std::cout << "Bullet " << num << ": pos=(" << x << "," << y << "), canExplode=" << b.canExplode << "\n";
        }
    }
    // Print two tanks
    if (map.isInMap(t1)) {
        auto [x, y] = t1.getPos();
        if (x >= 0 && x < ORIGIN_SIZE && y >= 0 && y < ORIGIN_SIZE)
            if(showDirection) grid[y][x] = t1.getSymbol();
            else grid[y][x] = t1.getLabel();
    }

    if (map.isInMap(t2)) {
        auto [x, y] = t2.getPos();
        if (x >= 0 && x < ORIGIN_SIZE && y >= 0 && y < ORIGIN_SIZE)
            if(showDirection) grid[y][x] = t2.getSymbol();
            else grid[y][x] = t2.getLabel();
    }

    std::cout << "Map (size: " << size << "x" << size << "):\n";
    for (int y = 0; y < ORIGIN_SIZE; y++) {
        for (int x = 0; x < ORIGIN_SIZE; x++) {
            std::cout<<grid[y][x]<<' ';
        }
        std::cout<<std::endl;
    }
    std::cout<<"Turn: "<<turn<<std::endl;
    std::cout << "Tank " << t1.getLabel() << " Life: " << t1.getLifePt() << " | Pos: (" << t1_x << "," << t1_y << ")"<<std::endl;
    std::cout << "Tank " << t2.getLabel() << " Life: " << t2.getLifePt() << " | Pos: (" << t2_x << "," << t2_y << ")"<<std::endl;
    std::cout << "Bullets: " << bullets.size() << std::endl;
    std::cout << "-------------------------------------------"<<std::endl;
}