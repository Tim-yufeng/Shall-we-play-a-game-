#pragma once
#include <utility>
#include "common.h"
#include "tank.h"
#include "map.h"

class Tank;

class Bullet{
    private:
    int x_pos, y_pos;
    Direction direction;

    public:
    bool canExplode;
    Bullet(int x, int y, Direction dir);

    std::pair<int, int> getPos() const;
    Direction getDir() const;
    void move();
    bool isHit(const Tank& tank);
    void explode();
    void bulletInMap(Map& map);
};



