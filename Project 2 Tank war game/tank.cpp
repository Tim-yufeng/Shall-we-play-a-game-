#include<iostream>
#include "tank.h"
#include "bullet.h"
#include "common.h"
Tank::Tank(int lifept, int x, int y, char l, Direction dir){ // constructor
        lifePt=lifept;
        x_pos=x;
        y_pos=y;
        fireCD=0;
        label=l;
        direction=dir;
    }

 // function for getting private property
 int Tank::getLifePt() const{
    return lifePt;
 }
 std::pair<int, int> Tank::getPos() const{
    return {x_pos, y_pos};
 }
 int Tank::getFireCD() const{
    return fireCD;
 }
 Direction Tank::getDirection() const{
    return direction;
 }
 char Tank::getLabel() const{
    return label;
 }
 char Tank::getSymbol() const{
    if(direction==D_Up) return '^';
    else if(direction==D_Down) return 'v';
    else if(direction==D_Left) return '<';
    else if(direction==D_Right) return '>';
    else return '?';
 }

 // function for moving 
 void Tank::move(Move move_dir){
    int new_x_pos=x_pos, new_y_pos=y_pos;
    if(move_dir == M_Forward){  
        if(direction == D_Up) new_y_pos--;
        else if(direction == D_Down) new_y_pos++;
        else if(direction == D_Left) new_x_pos--;
        else if(direction == D_Right) new_x_pos++;      
    }
    else if(move_dir == M_Left){
        if(direction == D_Up){
            direction=D_Left;
            new_x_pos--;
        }
        else if(direction == D_Down){
            direction=D_Right;
            new_x_pos++;
        }
        else if(direction == D_Left){
            direction=D_Down;
            new_y_pos++;
        }
        else if(direction == D_Right){
            direction=D_Up;
            new_y_pos--;
        }
    }
    else if(move_dir == M_Right){
        if(direction == D_Up){
            direction=D_Right;
            new_x_pos++;
        }
        else if(direction == D_Down){
            direction=D_Left;
            new_x_pos--;
        }
        else if(direction == D_Left){
            direction=D_Up;
            new_y_pos--;
        }
        else if(direction == D_Right){
            direction=D_Down;
            new_y_pos++;
        }
    }
    if(new_x_pos>=0 && new_x_pos<MAX_SIZE && new_y_pos>=0 && new_y_pos<MAX_SIZE){ // ensure within the initial map
        x_pos=new_x_pos;
        y_pos=new_y_pos;
    }
 }

 // function for firing
 Bullet Tank::make_fire(){
    int bullet_x=x_pos , bullet_y=y_pos ;
    fireCD=3;
    return Bullet(bullet_x, bullet_y, direction);
 }
 void Tank::bulletCoolDown(){
    fireCD--;
 }

 // tank reveiving life point deduction
 void Tank::takeDamage(int damage){
    if(lifePt>damage){
        lifePt-=damage;
        if(damage==2){  // damaged by enemy's bullet
            std::cout << RED << "[Tank "<<label<<" took a hit!] -2 HP" << RESET << std::endl;
        }
        else if (damage==1){ // damaged due to map shrink
            std::cout << RED << "[Tank "<<label<<" outside map!] -1 HP" << RESET << std::endl;
        }
        
    }
    else lifePt=0;
 }

 // judging whether tank is alive
 bool Tank::isAlive(){
    if(lifePt<=0) return false;
    else return true;
 }