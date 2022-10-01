#pragma once

typedef struct config_t {
    char *connection_string;
    char **words;
    size_t words_size;
} config_t;

config_t get_config();
void free_config(config_t config);

