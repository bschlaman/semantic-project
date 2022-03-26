package main

import (
	"io"
	"net/http"
	"os"

	"github.com/bschlaman/b-utils/pkg/logger"
	"github.com/bschlaman/b-utils/pkg/utils"
)

const (
	serverName string = "SEMANTIC-SERVER"
	port       string = ":8081"
	logPath    string = "logs/output.log"
	configPath string = "config.json"
	staticDir  string = "assets/static"
)

var log *logger.BLogger

func init() {
	file, err := os.OpenFile(logPath, os.O_APPEND|os.O_WRONLY, 0644)
	if err != nil {
		panic(err)
	}
	mw := io.MultiWriter(file, os.Stdout)
	log = logger.New(mw)
}

func main() {
	http.Handle("/echo", utils.LogReq(log)(utils.EchoHandle()))
	// http.Handle("/get_words", utils.LogReq(log)(getWordsHandle()))
	log.Info("starting http server on port", port)
	log.Fatal(http.ListenAndServe(port, nil))
}
