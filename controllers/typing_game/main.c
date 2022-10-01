#include <stdio.h>
#include <stdlib.h>
#include <pthread.h>
#include "./config.h"
#include "./netty.h"
#include "./consts.h"

config_t config;

static void *__move_snake(void *movement_ptr_raw)
{
    movement_t *movement_ptr = (movement_t *) movement_ptr_raw;

    transmit_movement(config, *movement_ptr);

    free(movement_ptr_raw);
    pthread_detach(pthread_self());
    pthread_exit(NULL);
    return NULL;
}

static void move_snake(movement_t movement)
{
    pthread_t t;
    movement_t *ptr = malloc(sizeof * ptr);
    if (ptr == NULL) {
        puts("Malloc is kil");
        exit(1);
    }
    *ptr = movement;

    if (pthread_create(&t, NULL, &__move_snake, ptr) != 0) {
        puts("Pthread is kil");
        exit(1);
    }
}

int main(int argc, char **argv)
{
    config = get_config();
    move_snake(X_PLUS);

    for (int i = 0; i < config.words_size; i++) {
        puts(config.words[i]);
    }

    free_config(config);
    return 0;
}
