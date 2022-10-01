project(TypingSnake LANGUAGES C)
set(SRC "./main.c"
  "./config.h"
  "./config.c"
  "./netty.h"
  "./netty.c"
  "./consts.h"
  "./consts.c")
set(LIBS "pthread" "ncurses" "curl")

add_executable(typing_snake ${SRC})
target_link_libraries(typing_snake ${LIBS})
