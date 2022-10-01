#include "./consts.h"

const char *movement_to_str(movement_t str)
{
    switch(str) {
    case X_PLUS:
        return "x+";
    case X_MINUS:
        return "x-";
    case Y_PLUS:
        return "y+";
    case Y_MINUS:
        return "y-";
    default:
        return "shit is broken :(";
    }
}
