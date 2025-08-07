#pragma once
#include<iostream>
#include<vector>
#include "tank.h"
#include "map.h"
#include "bullet.h"
#include "Renderer.h"
#include "common.h"
#include "AI.h"
class Tank;
class Bullet;

 // define game class 
class Game{
    private:
    GameMode game_mode;
    const char *file_name;
    Map map;
    Tank tankA, tankB;
    AI ai;
    std::vector<Bullet> bullets;
    Renderer renderer;
    Move dir_A, dir_B;
    int turn;
    bool gameOver=false;
    int gameResult; // 1: tankA won  2: tankB won  3: draw
    
    public:
    Game(GameMode, int, const char*);
    bool showDirection = false;
    int getTurn();
    void start();
    void nextTurn();
    void handleInput();
    void moveBullets();
    void detectTankCollision();
    void detectBulletHits();
    void checkShrink();
    void removeUsedBullet();
    bool judgeGame();
    void showGameResult();
    void save(std::string fileName);
    void load(std::string fileName);
    void log();
    void clearLogFile();
};
