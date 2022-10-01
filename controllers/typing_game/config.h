#pragma once

typedef struct config_t {
    char *connection_string;
} config_t;

config_t get_config();

