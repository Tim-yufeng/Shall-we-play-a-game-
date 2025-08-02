#pragma once
#include<vector>
#include "tank.h"
#include "bullet.h"
#include "map.h"

class Renderer {
public:
    void render(const Map&, const Tank&, const Tank&, const std::vector<Bullet>&, bool showDirection, int turn);   
};
