#pragma once
class Tank;

class Map{
    private:
    int size, turn=1;
    public:
    Map(int s);
    int getSize() const;
    int getTurn() const;
    void shrink();
    bool isInMap(const Tank& tank) const;
};