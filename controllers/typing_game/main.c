#include <stdio.h>
#include <stdlib.h>
#include <string.h>
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

typedef struct cardinal_words_t {
    char *left_word, *right_word, *up_word, *down_word;
} cardinal_words_t;

static char *get_word()
{
    int index = abs(rand());
    char *ret = config.words[index % config.words_size];
    return ret;
}

static cardinal_words_t get_words()
{
    cardinal_words_t ret;
    ret.left_word = get_word();
    ret.right_word = get_word();
    ret.up_word = get_word();
    ret.down_word = get_word();
    return ret;
}

static void game_iteration(cardinal_words_t *words)
{
    char buffer[1024];

    printf("\t\tUp: %s\n", words->up_word);
    printf("Left: %s \t\tRight: %s\n", words->left_word, words->right_word);
    printf("\t\tDown: %s\n", words->down_word);

    fgets(buffer, sizeof(buffer), stdin);
    buffer[strlen(buffer) - 1] = 0;

    if (strncmp(buffer, words->left_word, sizeof(buffer)) == 0) {
        move_snake(X_MINUS);
        words->left_word = get_word();
        puts("Moving left");
    } else if (strncmp(buffer, words->right_word, sizeof(buffer)) == 0) {
        move_snake(X_PLUS);
        words->right_word = get_word();
        puts("Moving right");
    } else if (strncmp(buffer, words->up_word, sizeof(buffer)) == 0) {
        move_snake(Y_PLUS);
        words->up_word = get_word();
        puts("Moving up");
    } else if (strncmp(buffer, words->down_word, sizeof(buffer)) == 0) {
        move_snake(Y_MINUS);
        words->down_word = get_word();
        puts("Moving down");
    } else {
        puts("No more snake for you");
        exit(1);
    }
}

static void game_loop()
{
    cardinal_words_t words = get_words();
    for (;;) {
        game_iteration(&words);
    }
}

int main(int argc, char **argv)
{
    srand(time(NULL));
    config = get_config();
    game_loop();
    free_config(config);
    return 0;
}
