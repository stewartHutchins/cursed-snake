#include <stdio.h>
#include <stdlib.h>
#include "./config.h"
#include "./netty.h"
#include "./consts.h"

int main(int argc, char **argv)
{
    config_t config = get_config();
    int res = transmit_movement(config, X_PLUS);

    for (int i = 0; i < config.words_size; i++) {
      puts(config.words[i]);
    }

    free_config(config);
    return res ? 0 : 1;
}
