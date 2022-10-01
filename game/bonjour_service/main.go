package main

import (
	"log"
	"os"
	"os/signal"
	"time"

	"github.com/oleksandr/bonjour"
)

func main() {
	// Run registration (blocking call)
	s, err := bonjour.Register("CursedSnake", "_snake._tcp", "", 6969, []string{"txtv=1", "app=snake"}, nil)
	if err != nil {
		log.Fatalln(err.Error())
	}

	// Ctrl+C handling
  log.Println("Waiting for exit...");
	handler := make(chan os.Signal, 1)
	signal.Notify(handler, os.Interrupt)
	for sig := range handler {
		if sig == os.Interrupt {
      log.Println("Shutting Down");
			s.Shutdown()
			time.Sleep(1e9)
			break
		}
	}
}
