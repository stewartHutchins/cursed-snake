project(TypingSnake LANGUAGES C)
cmake_minimum_required(VERSION 3.24)
set(SRC "./main.c"
  "./config.h"
  "./config.c"
  "./netty.h"
  "./netty.c"
  "./consts.h"
  "./consts.c")
set(LIBS "pthread" "ncurses" "curl")

set(COMPILER_FLAGS "-Wall -Wextra -Wpedantic -Werror")
set(CMAKE_C_FLAGS_DEBUG "-g -O0 ${COMPILER_FLAGS} -DDEBUG")
set(CMAKE_C_FLAGS_RELEASE "-O2 ${COMPILER_FLAGS}")

file(COPY "${CMAKE_SOURCE_DIR}/script.txt" DESTINATION "${CMAKE_BINARY_DIR}")
add_executable(typing_snake ${SRC})
target_link_libraries(typing_snake ${LIBS})
