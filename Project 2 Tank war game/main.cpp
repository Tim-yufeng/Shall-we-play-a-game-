#include<vector>
#include<cstring>
#include <getopt.h>
#include "Renderer.h"
#include "tank.h"
#include "bullet.h"
#include "map.h"
#include "game.h"
#include "common.h"

void print_help(){
std::cout<<"Usage: ./tankwar [options](optional)\n";
std::cout<<"Options:\n";
std::cout<<"  -h | --help              Print this help message and exit.\n";
std::cout<<"  --log-file <file>       Log the game process to a file. (Default: tankwar.log)\n";
std::cout<<"   -m <mode> | --mode=<mode>       Specify the game mode (PVP/PVE/DEMO). (Default: PVP)\n";
std::cout<<"   -p <point> | --initial-life=<point>  Specify the initial life points of the tanks. \n(Default: 5)\n";
}


int main(int argc, char *argv[]) {
    int opt;
    const char* log_file="tankwar.log";   // default log file
    GameMode mode = PVP;
    int init_lifept=5;   // default initial life point
    bool show_help=false;

    const struct option long_options[] = {
    {"help",        no_argument,       nullptr, 'h'},
    {"log-file",    required_argument, nullptr, 'l'},
    {"mode",        required_argument, nullptr, 'm'},
    {"initial-life",required_argument, nullptr, 'p'},
    {nullptr,       0,                 nullptr,  0}  
};
    const char* optstring="hl:m:p:";
    while ((opt = getopt_long(argc, argv, optstring, long_options, nullptr)) != -1) {
    switch (opt) {
        case 'h':
            show_help = true;
            break;
        case 'l':
            log_file = optarg;  
            break;
        case 'm':
            if (strcmp(optarg, "PVP") == 0) {
                mode = PVP;
            } else if (strcmp(optarg, "PVE") == 0) {
                mode = PVE;
            } else if (strcmp(optarg, "DEMO") == 0) {
                mode = DEMO;
            } else {
                std::cerr << "Invalid mode. Use PVP, PVE or DEMO\n";
                return 1;
            }
            break;
        case 'p':
            init_lifept = atoi(optarg);  
            break;
        case '?':  // unknown command
            return 1;
        default:
            std::cerr << "?? getopt_long returned unexpected value\n";
            return 1;
    }
}
if(show_help){
    print_help();
    return 0;
}
std::cout <<"\033[96;1m"<< "You have chosen:\n"   // print config information
          << "  Log file: " << log_file << "\n"
          << "  Game mode: " << (mode == PVP ? "PVP" : (mode == PVE ? "PVE" : "DEMO")) << "\n"
          << "  Initial life: " << init_lifept << "\n"<<RESET;

    Game game(mode, init_lifept, log_file);
    game.start();
    return 0;
}

