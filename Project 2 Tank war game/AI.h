#pragma once
#include "tank.h"
#include "common.h"
#include "map.h"
class Game;

class AI{
public:
    Move getMove(const Tank& aiTank, const Tank& playerTank, const Map& map, const std::vector<Bullet>& bullets);
};