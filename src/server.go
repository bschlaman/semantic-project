package main

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"os"

	"github.com/bschlaman/b-utils/pkg/logger"
	"github.com/bschlaman/b-utils/pkg/utils"
	"github.com/jackc/pgx/v4"
)

const (
	serverName string = "SEMANTIC-SERVER"
	port       string = ":8081"
	logPath    string = "logs/output.log"
	configPath string = "config.json"
	staticDir  string = "assets/static"
)

var log *logger.BLogger

func getWordsHandle() http.Handler {
	return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
		conn, err := pgx.Connect(context.Background(), os.Getenv("DATABASE_URL"))
		if err != nil {
			fmt.Fprintf(os.Stderr, "Unable to connect to database: %v\n", err)
			os.Exit(1)
		}
		defer conn.Close(context.Background())

		var id, word1, word2 string
		err = conn.QueryRow(context.Background(), "select id, word1, word2 from words limit 1").Scan(&id, &word1, &word2)
		if err != nil {
			fmt.Fprintf(os.Stderr, "QueryRow failed: %v\n", err)
			os.Exit(1)
		}

		fmt.Fprintln(w, id, word1, word2)
	})
}

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
	http.Handle("/get_words", utils.LogReq(log)(getWordsHandle()))
	log.Info("starting http server on port", port)
	log.Fatal(http.ListenAndServe(port, nil))
}
