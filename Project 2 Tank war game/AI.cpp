#include<iostream>
#include<queue>
#include<utility>
#include<unordered_map>
#include "AI.h"
#include "tank.h"
#include "map.h"
#include "bullet.h"
#include "common.h"
class Game;


Move getOutOfBoundary(const Tank& aiTank, const Map& map){
    auto [ai_x, ai_y] = aiTank.getPos();
    Direction curDir = aiTank.getDirection();

    if (map.isInMap(aiTank)) return M_Forward;

    const int dx[4] = {0, -1, 0, 1};   // Up, Left, Down, Right
    const int dy[4] = {-1, 0, 1, 0};

    const int SIZE = map.getSize();

    std::queue<std::pair<int, int>> q;
    std::unordered_map<int, std::pair<int, int>> parent;  // key = y * 100 + x
    std::vector<std::vector<bool>> visited(SIZE, std::vector<bool>(SIZE, false));

    q.push({ai_x, ai_y});
    visited[ai_y][ai_x] = true;

    std::pair<int, int> target = {-1, -1};

    // 1. BFS to find nearest valid cell
    while (!q.empty()) {
        auto [x, y] = q.front(); q.pop();
        if (MAX_SIZE-map.getSize()<=x && x<=map.getSize() && MAX_SIZE-map.getSize()<=y && y<=map.getSize()) {  // judge whether in map
            target = {x, y};
            break;
        }

        for (int d = 0; d < 4; ++d) {
            int nx = x + dx[d];
            int ny = y + dy[d];
            if (nx >= 0 && nx < SIZE && ny >= 0 && ny < SIZE && !visited[ny][nx]) {
                visited[ny][nx] = true;
                q.push({nx, ny});
                parent[ny * 100 + nx] = {x, y};
            }
        }
    }

    // 2. No way out?
    if (target.first == -1) return M_Forward;

    // 3. Backtrack path to get first move
    std::pair<int, int> pos = target;
    std::pair<int, int> prev = {-1, -1};

    while (parent.count(pos.second * 100 + pos.first) && parent[pos.second * 100 + pos.first] != std::make_pair(ai_x, ai_y)) {
        pos = parent[pos.second * 100 + pos.first];
    }
    prev = pos;  // First step from current position

    int dx1 = prev.first - ai_x;
    int dy1 = prev.second - ai_y;

    // 4. Get desired direction
    Direction targetDir;
    if (dx1 == 0 && dy1 == -1) targetDir = D_Up;
    else if (dx1 == -1 && dy1 == 0) targetDir = D_Left;
    else if (dx1 == 0 && dy1 == 1) targetDir = D_Down;
    else if (dx1 == 1 && dy1 == 0) targetDir = D_Right;
    else return M_Forward;  // fallback

    // 5. Convert to Move (relative to current direction)
    if (targetDir == curDir) return M_Forward;
    if ((curDir + 1) % 4 == targetDir) return M_Right;
    if ((curDir + 3) % 4 == targetDir) return M_Left;
    return M_Left;  // fallback
}

Move decideMove(const Tank& self, const Tank& enemy, const Map& map, const std::vector<Bullet>& bullets) {
    auto [x, y] = self.getPos();
    Direction dir = self.getDirection();
    int selfHP = self.getLifePt();
    int enemyHP = enemy.getLifePt();
    auto [ex, ey] = enemy.getPos();

    // ---- Step 1: Evade Bullets ----
    for (const Bullet& b : bullets) {
        auto [bx, by] = b.getPos();
        Direction bdir = b.getDir();

        // bullet flying toward me in the same column/row  MAX_SIZE-size<=x && x<=map.getSize() && MAX_SIZE-size<=y && y<=map.getSize()
        if (bdir == D_Up && bx == x && by > y && (MAX_SIZE-map.getSize()<=x && x<=map.getSize() && MAX_SIZE-map.getSize()<=y+1 && y+1<=map.getSize())) {
            return M_Left;
        }
        if (bdir == D_Down && bx == x && by < y && (MAX_SIZE-map.getSize()<=x && x<=map.getSize() && MAX_SIZE-map.getSize()<=y-1 && y-1<=map.getSize())) {
            return M_Right;
        }
        if (bdir == D_Left && by == y && bx > x && (MAX_SIZE-map.getSize()<=x && x<=map.getSize() && MAX_SIZE-map.getSize()<=y && y<=map.getSize())) {
            return M_Left;
        }
        if (bdir == D_Right && by == y && bx < x && (MAX_SIZE-map.getSize()<=x && x<=map.getSize() && MAX_SIZE-map.getSize()<=y-1 && y-1<=map.getSize())) {
            return M_Right;
        }
    }

    // ---- Step 2: Aggressive if stronger ----
    int dist = abs(x - ex) + abs(y - ey);
    if (selfHP > enemyHP && dist > 1) {
        // approach the enemy
        if (x < ex) return dir == D_Right ? M_Forward : M_Right;
        if (x > ex) return dir == D_Left  ? M_Forward : M_Left;
        if (y < ey) return dir == D_Down  ? M_Forward : M_Right;
        if (y > ey) return dir == D_Up    ? M_Forward : M_Left;
    }

    // ---- Step 3: Escape if weaker ----
    if (selfHP < enemyHP && dist < 5) {
        // escape
        if (x < ex) return dir == D_Left  ? M_Forward : M_Left;
        if (x > ex) return dir == D_Right ? M_Forward : M_Right;
        if (y < ey) return dir == D_Up    ? M_Forward : M_Left;
        if (y > ey) return dir == D_Down  ? M_Forward : M_Right;
    }

    // ---- Step 4: Default ----
    return M_Forward;
}

Move AI::getMove(const Tank& aiTank, const Tank& playerTank, const Map& map, const std::vector<Bullet>& bullets){
    auto [ai_x, ai_y]=aiTank.getPos();
    auto [player_x, player_y]=playerTank.getPos();
    Direction dir=aiTank.getDirection();
    if(!map.isInMap(aiTank)){
        return getOutOfBoundary(aiTank, map);
    }
    else
    return decideMove(aiTank, playerTank, map, bullets);

}