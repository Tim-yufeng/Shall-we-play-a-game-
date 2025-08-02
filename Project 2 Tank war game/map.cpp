#include<iostream>
#include "map.h"
#include "tank.h"
#include "common.h"
Map::Map(int s){
    size=s;
}

int Map::getSize() const{
    return size;
}
int Map::getTurn() const{
    return turn;
}
void Map::shrink(){
    size-=2;
}
bool Map::isInMap(const Tank& tank) const{
    auto [x, y]=tank.getPos();
    if(MAX_SIZE-size<=x && x<=size && MAX_SIZE-size<=y && y<=size) return true;
    else return false;
} 