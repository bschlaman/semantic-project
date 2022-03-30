package main

import (
	"context"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
	"path"

	"github.com/bschlaman/b-utils/pkg/logger"
	"github.com/bschlaman/b-utils/pkg/utils"
	"github.com/jackc/pgx/v4"
)

const (
	serverName string = "SEMANTIC-SERVER"
	port       string = ":8082"
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
		err = conn.QueryRow(context.Background(),
			`SELECT id, word1, word2 FROM words
			WHERE status = 'PENDING'::word_pair_status
			ORDER BY random() LIMIT 1`,
		).Scan(&id, &word1, &word2)
		if err != nil {
			log.Errorf("QueryRow failed: %v\n", err)
			http.Error(w, "something went wrong", http.StatusInternalServerError)
			return
		}

		js, err := json.Marshal(&struct {
			Id    string `json:"id"`
			Word1 string `json:"word1"`
			Word2 string `json:"word2"`
		}{
			id,
			word1,
			word2,
		})
		if err != nil {
			log.Errorf("json.Marshal failed: %v\n", err)
			http.Error(w, "something went wrong", http.StatusInternalServerError)
			return
		}
		w.Header().Set("Content-Type", "application/json")
		w.Write(js)
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
	fs := http.FileServer(http.Dir(path.Join("..", staticDir)))
	http.Handle("/", fs)
	http.Handle("/echo", utils.LogReq(log)(utils.EchoHandle()))
	http.Handle("/get_words", utils.LogReq(log)(getWordsHandle()))
	log.Info("starting http server on port", port)
	log.Fatal(http.ListenAndServe(port, nil))
}
