#include "./config.h"

config_t get_config()
{
    config_t ret;
    ret.connection_string = "http://192.168.3.7:6969";
    return ret;
}
