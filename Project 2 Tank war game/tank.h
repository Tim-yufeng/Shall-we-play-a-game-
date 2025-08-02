#pragma once
#include <utility>
// #include "game.h"
#include "bullet.h"
#include "common.h"
class Bullet;

class Tank{
    private:
    int lifePt, x_pos, y_pos, fireCD;
    Direction direction;
    char label;  // "A" or "B"
    public:
    Tank(int lifept, int x, int y, char l, Direction dir);
    int getLifePt() const;
    std::pair<int, int> getPos() const;
    int getFireCD() const;
    Direction getDirection() const;
    char getLabel() const;
    char getSymbol() const;

    Bullet make_fire();  
    void bulletCoolDown();
    void move(Move move_dir);
    void takeDamage(int damage);
    bool isAlive();
 };