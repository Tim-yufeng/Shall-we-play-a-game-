#include<iostream>
#include<vector>
#include<algorithm>
#include <thread>
#include <chrono>
#include "game.h"
#include "tank.h"
#include "map.h"
#include "bullet.h"
#include "Renderer.h"
// #include "AI.h"

Game::Game(GameMode mode=PVP, int init_lifept=5) : game_mode(mode), map(20), tankA(init_lifept,12,12,'A',D_Up), tankB(init_lifept,6,6,'B',D_Up), 
 dir_A(M_Invalid), dir_B(M_Invalid), turn(1), gameResult(0) {}                                                         // initial config of two tanks' position and direction


int Game::getTurn(){
    return turn;
}

void Game::start(){
    while(gameOver==false){
        renderer.render(map, tankA, tankB, bullets, showDirection, turn);
        handleInput();
        nextTurn();
        if(judgeGame()) break;
        turn++;
        if(game_mode==DEMO) std::this_thread::sleep_for(std::chrono::milliseconds(500));  // wait for 0.5 seconds
    }
    renderer.render(map, tankA, tankB, bullets, showDirection, turn);  // display again before game ends
    std::cout<<"\033[1;31m Game over! \033[0m\n"<<"\n"<<RESET;
    showGameResult();
    
}
void Game::nextTurn(){
    tankA.move(dir_A);
    tankB.move(dir_B);
    detectTankCollision();
    if(tankA.getFireCD()==0){
        bullets.push_back(tankA.make_fire());  // generate new bullet
    }
    else tankA.bulletCoolDown();

    if(tankB.getFireCD()==0){
        bullets.push_back(tankB.make_fire());  // generate new bullet
    }
    else tankB.bulletCoolDown();
    if(!bullets.empty()) moveBullets();
    detectBulletHits();
    removeUsedBullet();

    checkShrink();
}

void Game::handleInput(){
    
    bool valid=false;

    // player A's turn
    while (!valid)
    {
    if(game_mode==DEMO){
        dir_A=ai.getMove(tankA, tankB, map, bullets);
        valid=true;
    }
    else{
    std::cout << RED << "[Player A]" << RESET << "Enter move (f:forward, l:left, r:right, dir:show direction, lab:show label): ";
    std::string cmd1;
    std::cin>>cmd1;
    if(cmd1=="move"){
        char move_dir;
        std::cin>>move_dir;
        if(move_dir=='f'){ // 'f' for move upward
            dir_A=M_Forward;
            valid=true;
        }
        else if(move_dir=='l'){ // 'l' for move left
            dir_A=M_Left;
            valid=true;
        }
        else if(move_dir=='r'){ // 'r' for move right
            dir_A=M_Right;
            valid=true;
        }
        else std::cout<<"Invalid input. Try again.\n";
    }
    else if(cmd1=="lab"){
        showDirection=false;
        renderer.render(map, tankA, tankB, bullets, showDirection, turn);
        std::cout << "Direction display mode enabled.\n";
        continue;
    }
    else if(cmd1=="dir"){
        showDirection=true;
        renderer.render(map, tankA, tankB, bullets, showDirection, turn);
        std::cout << "Direction display mode enabled.\n";
        continue;
    }
    else {
        std::cout<<"Invalid input. Try again.\n";
        continue;
    }
    }
}
    valid=false;
    // player B's turn
    
    while (!valid)
    {
        if(game_mode!=PVP){
        dir_B=ai.getMove(tankB, tankA, map, bullets);
        valid=true;
    }
    else{
    std::cout << BLUE << "[Player B]" << RESET << "Enter move (f:forward, l:left, r:right, dir:show direction, lab:show label): ";
    std::string cmd2;
    std::cin>>cmd2;
    if(cmd2=="move"){
        char move_dir;
        std::cin>>move_dir;
        if(move_dir=='f'){ // 'f' for move upward
            dir_B=M_Forward;
            valid=true;
        }
        else if(move_dir=='l'){ // 'l' for move left
            dir_B=M_Left;
            valid=true;
        }
        else if(move_dir=='r'){ // 'r' for move right
            dir_B=M_Right;
            valid=true;
        }
        else std::cout<<"Invalid input. Try again.\n";
    }
    else if(cmd2=="lab"){
        showDirection=false;
        renderer.render(map, tankA, tankB, bullets, showDirection,turn);
        std::cout << "Direction display mode enabled.\n";
        continue;
    }
    else if(cmd2=="dir"){
        showDirection=true;
        renderer.render(map, tankA, tankB, bullets, showDirection,turn);
        std::cout << "Direction display mode enabled.\n";
        continue;
    }
    else {
        std::cout<<"Invalid input. Try again.\n";
        continue;
    }
    }
    }
}

void Game::moveBullets(){
    for(Bullet& b : bullets){
        if(b.canExplode) {
            b.move();
        }
    }
}
void Game::detectTankCollision(){
    if(tankA.getPos()==tankB.getPos()){
        if(tankA.getLifePt()>tankB.getLifePt()){
            // std::cout<<"Tank A won due to collision!\n";
            gameResult=1; 
        }
        else if(tankA.getLifePt()<tankB.getLifePt()){
            // std::cout<<"Tank B won due to collision!\n";
            gameResult=2;
        }
        // else std::cout<<"Draw due to collision!\n";
        else gameResult=3;
        gameOver=true;
    }

}
void Game::detectBulletHits(){
    for(Bullet& b : bullets){
        b.bulletInMap(map);
        if(!b.canExplode) continue; 

        if(b.isHit(tankA)){
            tankA.takeDamage(2);
            b.explode();
        }
        if(b.isHit(tankB)){
            tankB.takeDamage(2);
            b.explode();
        }
    }
}
 void Game::checkShrink(){
    if(turn%16==0){
        map.shrink();
    }
    if(!map.isInMap(tankA)){
        tankA.takeDamage(1);
    }
    if(!map.isInMap(tankB)){
        tankB.takeDamage(1);
    }
 }
 void Game::removeUsedBullet(){
    bullets.erase(std::remove_if(bullets.begin(), bullets.end(),
    [](const Bullet& b) { return !b.canExplode; }), bullets.end());

 }

bool Game::judgeGame(){    // false if not over, otherwise true
    if(!(tankA.isAlive() && tankB.isAlive())){
        gameOver=true;
        if((!tankA.isAlive()) && tankB.isAlive()){
            // std::cout<<"Tank B won!\n";/
            gameResult=2;
        }
        else if((!tankB.isAlive()) && tankA.isAlive()){
            // std::cout<<"Tank A won!\n";
            gameResult=1;
        }
        // else std::cout<<"Draw! Good game!\n";
        else gameResult=3;
        return true;
    }
    return false;
}

void Game::showGameResult(){
    if(gameResult==1) std::cout<<"\033[1;31m Tank A won! \033[0m\n"<<"\n"<<RESET;
    else if(gameResult==2) std::cout<<"\033[1;31m Tank B won! \033[0m\n"<<"\n"<<RESET;
    else if(gameResult==3) std::cout<<"\033[1;31m Draw! Good game! \033[0m\n"<<"\n"<<RESET;
}

