package main

import (
	"net/http"
	"os"

	log "github.com/bschlaman/b-utils/pkg/logger"
	"github.com/bschlaman/b-utils/pkg/utils"
)

const (
	serverName string = "SEMANTIC-SERVER"
	port       string = ":8080"
	logPath    string = "logs/output.log"
	configPath string = "config.json"
	staticDir  string = "assets/static"
)

var logger *log.BLogger

func init() {
	// Print something to stdout for testing purposes
	println(" ### Starting", serverName, "on port", port)

	file, err := os.OpenFile(logPath, os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		panic(err)
	}
	logger.Info(" ### Starting", serverName, "on port", port)
}

func main() {
	http.Handle("/echo", utils.LogReq(logger)(utils.EchoHandle()))
	// http.Handle("/get_words", utils.LogReq(logger)(getWordsHandle()))
	logger.Info("starting http server on port", port)
	logger.Fatal(http.ListenAndServe(port, nil))
}
