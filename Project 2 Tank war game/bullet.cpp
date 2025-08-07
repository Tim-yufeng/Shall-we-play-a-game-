#include<iostream>
#include "bullet.h"
#include "common.h"
#include "tank.h"
#include "map.h"
Bullet::Bullet(int x, int y, Direction dir){  // constructor
        x_pos=x; 
        y_pos=y;
        direction=dir;
        canExplode=true;
    }
 // function for getting private property
std::pair<int, int> Bullet::getPos() const{
    return {x_pos, y_pos};
}
Direction Bullet::getDir() const{
    return direction;
}
// function for moving
void Bullet::move(){
    int new_x_pos=x_pos, new_y_pos=y_pos;
    if(direction==D_Up) new_y_pos-=2;
    else if(direction==D_Down) new_y_pos+=2;
    else if(direction==D_Left) new_x_pos-=2;
    else if(direction==D_Right) new_x_pos+=2;
    if(new_x_pos>=0 && new_x_pos<MAX_SIZE && new_y_pos>=0 && new_y_pos<MAX_SIZE){ // ensure within the initial map
        x_pos=new_x_pos;
        y_pos=new_y_pos;
    }
    else canExplode=false;  // become invalid if the bullet is going to leave the map
}
bool Bullet::isHit(const Tank& tank){
    // int tank_x_pos, tank_y_pos;
    int pre_x_pos, pre_y_pos;
    if(direction==D_Up){     // judge whether there is hit during the flying between two turns
        pre_x_pos=x_pos;
        pre_y_pos=y_pos+1;
    }
    else if(direction==D_Down){
        pre_x_pos=x_pos;
        pre_y_pos=y_pos-1;
    }
    else if(direction==D_Left){
        pre_x_pos=x_pos+1;
        pre_y_pos=y_pos;
    }
    else if(direction==D_Right){
        pre_x_pos=x_pos-1;
        pre_y_pos=y_pos;
    }
    auto [tank_x_pos, tank_y_pos]=tank.getPos();
    if((x_pos == tank_x_pos && y_pos == tank_y_pos) || (pre_x_pos == tank_x_pos && pre_y_pos == tank_y_pos))
    return true;
    else return false;
}
void Bullet::explode(){
    canExplode=false;
}
void Bullet::bulletInMap(Map& map){   // disable bullets that is out of map
    if(!(x_pos>=0 && x_pos<=map.getSize() && y_pos>=0 && y_pos<=map.getSize()))
    canExplode=false;
}