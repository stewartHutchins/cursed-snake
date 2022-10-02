# cursed-snake
## Snake Server
```bash
# bash # fish doesnt work :-(
make setup-dev
. .venv/bin/activate
python -m cursed_snake
```

## Android App
Put on your phone (good luck)

Set the text edit at the bottom of the app to the last number of the ip (x.x.x.THIS).

## Typing Game
Edit config.c to have the right IP (canny be bothered)
`
```bash
# cd controller/typing_snake
mkdir -p build
cd build
cmake ..
cmake --build . -j
./typing_snake
```

Then type the word next to the way you want to go

## Beer-troller
Put on an ESP32 then plug some cups in. (idK)
