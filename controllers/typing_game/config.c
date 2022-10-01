#include <stdlib.h>
#include <stdio.h>
#include <ctype.h>
#include <string.h>
#include "./config.h"

/*
typedef struct config_t {
    char *connection_string;
    char **words;
    size_t words_size;
} config_t;
*/

#define SCRIPT "./script.txt"

static char *read_next_word(FILE *f)
{
    char buffer[1024];

    int i = 0;
    for (int c; c = fgetc(f), c != EOF && i < sizeof(buffer);) {
        if (isalpha(c = tolower(c))) {
            buffer[i++] = c;
        } else if ((c == ' ' || c == '\n') && i != 0) {
            break;
        }
    }

    buffer[i] = 0;

    if (i != 0) {
        char *ret = malloc(sizeof * ret * (i + 1));
        if (ret != NULL) {
            strcpy(ret, buffer);
        }

        return ret;
    } else {
        return NULL;
    }
}

config_t get_config()
{
    config_t ret;
    ret.connection_string = "http://192.168.3.7:6969";
    ret.words = malloc(sizeof(*ret.words));
    ret.words_size = 0;

    FILE *f = fopen(SCRIPT, "r");
    if (f == NULL) {
      puts("Error, no bee movie script.txt");
      exit(1);
    }

    for (char *word; word = read_next_word(f), word != NULL; ret.words_size++) {
        ret.words = realloc(ret.words, sizeof(ret.words) * (ret.words_size + 1));
        ret.words[ret.words_size] = word;
    }
    fclose(f);

    return ret;
}

void free_config(config_t config)
{
    for (int i = 0; i < config.words_size; i++) {
        if (config.words[i] != NULL) {
            free(config.words[i]);
        }
    }
    free(config.words);
}
