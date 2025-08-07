#include<iostream>
#include<vector>
#include<algorithm>
#include<thread>
#include<chrono>
#include<fstream>
#include<sstream>
#include "game.h"
#include "tank.h"
#include "map.h"
#include "bullet.h"
#include "Renderer.h"

Game::Game(GameMode mode=PVP, int init_lifept=5, const char* log_file="tankwar.log") : game_mode(mode),file_name(log_file), map(20), tankA(init_lifept,12,12,'A',D_Up), tankB(init_lifept,6,6,'B',D_Up), 
 dir_A(M_Invalid), dir_B(M_Invalid), turn(1), gameResult(0) {}                                                         // initial config of two tanks' position and direction

int Game::getTurn(){
    return turn;
}

void Game::start(){
    clearLogFile(); // clear the remaining content
    while(gameOver==false){
        renderer.render(map, tankA, tankB, bullets, showDirection, turn);
        handleInput();
        nextTurn();
        if(judgeGame()) break;
        if(game_mode==DEMO) std::this_thread::sleep_for(std::chrono::milliseconds(750));  // wait for 0.5 seconds
        log();
        turn++;
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
    std::cout << RED << "[Player A]" << RESET << "Please enter (f:forward, l:left, r:right, dir:show direction, lab:show label): ";
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
    else if(cmd1=="lab"){       // show tank label
        showDirection=false;
        renderer.render(map, tankA, tankB, bullets, showDirection, turn);
        std::cout << "Direction display mode enabled.\n";
        continue;
    }
    else if(cmd1=="dir"){       // show tank direction
        showDirection=true;
        renderer.render(map, tankA, tankB, bullets, showDirection, turn);
        std::cout << "Direction display mode enabled.\n";
        continue;
    }
    else if(cmd1=="save"){         // save game state to a file
        std::string fileName;
        std::cin>>fileName;
        save(fileName);
    }
    else if(cmd1=="load"){      // load game state from a file
        std::string fileName;
        std::cin>>fileName;
        load(fileName);
        renderer.render(map, tankA, tankB, bullets, showDirection, turn);

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
    std::cout << BLUE << "[Player B]" << RESET << "Please enter (f:forward, l:left, r:right, dir:show direction, lab:show label): ";
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
    else if(cmd2=="lab"){      // show tank label
        showDirection=false;
        renderer.render(map, tankA, tankB, bullets, showDirection,turn);
        std::cout << "Direction display mode enabled.\n";
        continue;
    }
    else if(cmd2=="dir"){          // show tank direction
        showDirection=true;
        renderer.render(map, tankA, tankB, bullets, showDirection,turn);
        std::cout << "Direction display mode enabled.\n";
        continue;
    }
    else if(cmd2=="save"){      // save game state to a file
        std::string fileName;
        std::cin>>fileName;
        save(fileName);
    }
    else if(cmd2=="load"){      //  load game from a file
        std::string fileName;
        std::cin>>fileName;
        load(fileName);
        renderer.render(map, tankA, tankB, bullets, showDirection, turn);

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
        if(tankA.getLifePt()>tankB.getLifePt()){  // gameResult=1: A won, gameResult=2: B won, gameResult=3: draw
            gameResult=1; 
            tankB.takeDamage(tankB.getLifePt()); // life point deducted to 0
        }
        else if(tankA.getLifePt()<tankB.getLifePt()){
            gameResult=2;
            tankA.takeDamage(tankA.getLifePt());
        }
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
        else if(b.isHit(tankB)){
            tankB.takeDamage(2);
            b.explode();
        }
    }
}
 void Game::checkShrink(){      // control map's shrinking and life point deduction due to outside map
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
 void Game::removeUsedBullet(){     // delete invalid bullets
    bullets.erase(std::remove_if(bullets.begin(), bullets.end(),
    [](const Bullet& b) { return !b.canExplode; }), bullets.end());
 }

bool Game::judgeGame(){    // false if not over, otherwise true
    if(!(tankA.isAlive() && tankB.isAlive())){
        gameOver=true;
        if((!tankA.isAlive()) && tankB.isAlive()){
            gameResult=2;
        }
        else if((!tankB.isAlive()) && tankA.isAlive()){
            gameResult=1;
        }
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

/*
save format:
<game_mode>
(A's) <current lifept> <x_pos> <y_pos> <direction>
(B's) <current lifept> <x_pos> <y_pos> <direction>
<turn>
<size>
<bullets list>(format: <x_pos> <y_pos> <direction>)
*/

void Game::save(std::string fileName) {
    std::ofstream saveFile(fileName);
    if (saveFile.is_open()) {
        auto [xA, yA] = tankA.getPos();
        auto [xB, yB] = tankB.getPos();

        saveFile << static_cast<int>(game_mode) << std::endl;
        saveFile << tankA.getLifePt() << " " << xA << " " << yA << " " << static_cast<int>(tankA.getDirection()) << std::endl;
        saveFile << tankB.getLifePt() << " " << xB << " " << yB << " " << static_cast<int>(tankB.getDirection()) << std::endl;
        saveFile << turn << std::endl;
        saveFile << map.getSize() << std::endl;

        for (const Bullet& b : bullets) {
            auto [x, y] = b.getPos();
            saveFile << x << " " << y << " " << static_cast<int>(b.getDir()) << std::endl;
        }

        saveFile.close();
        std::cout << "Game saved successfully!\n";
    } else {
        std::cout << "Failed to save the game.\n";
    }
}

void Game::load(std::string fileName) {
    std::ifstream load_game(fileName);
    if (!load_game.is_open()) {
        std::cout << "Failed to load the game.\n";
        return;
    }

    int mode_int, dirA_int, dirB_int;
    int tankA_lifept, tankB_lifept, tankA_x, tankA_y, tankB_x, tankB_y;
    int loaded_turn, loaded_size;

    load_game >> mode_int;
    game_mode = static_cast<GameMode>(mode_int);

    load_game >> tankA_lifept >> tankA_x >> tankA_y >> dirA_int;
    load_game >> tankB_lifept >> tankB_x >> tankB_y >> dirB_int;
    load_game >> loaded_turn;
    load_game >> loaded_size;

    // refresh tank and map
    map = Map(loaded_size);
    tankA = Tank(tankA_lifept, tankA_x, tankA_y, 'A', static_cast<Direction>(dirA_int));
    tankB = Tank(tankB_lifept, tankB_x, tankB_y, 'B', static_cast<Direction>(dirB_int));
    turn = loaded_turn;

    // refresh bullets
    bullets.clear();
    int x, y, dir_int;
    while (load_game >> x >> y >> dir_int) {
        bullets.emplace_back(x, y, static_cast<Direction>(dir_int));
    }

    load_game.close();
    std::cout << "Successfully loaded!\n";
}


std::string num2Dir(Direction num){     // function for converting Direction number to direction string
    if(num==D_Up) return "Up";
    else if(num==D_Down) return "Down";
    else if(num==D_Left) return "Left";
    else return "Right";
}

/*
log format:
Turn: <turn>
TankA: 
Current life point: <life point>, Current position: <coordinate>, Current direction: <direction>
TankB: 
Current life point: <life point>, Current position: <coordinate>, Current direction: <direction>
*/
void Game::log(){       // log game process to a file
    std::ofstream logFile(file_name, std::ios::app);
    if (logFile.is_open()) {
        auto [xA, yA] = tankA.getPos();
        auto [xB, yB] = tankB.getPos();
        logFile << "Turn: " << turn << std::endl;
        logFile << "TankA: \n" << "Current life point: " << tankA.getLifePt() << ", Current position: (" << xA << ", " << yA << "), Current direction: " << num2Dir(tankA.getDirection()) << std::endl;
        logFile << "TankB: \n" << "Current life point: " << tankB.getLifePt() << " Current position: (" << xB << ", " << yB << ") Current direction: " << num2Dir(tankB.getDirection()) << std::endl;
        logFile << "--------------------------------------------------------------------------\n";

        logFile.close();
    } 
}

void Game::clearLogFile(){    // clear last turn's log information
    std::ofstream file(file_name, std::ios::trunc);
    file.close();
}


