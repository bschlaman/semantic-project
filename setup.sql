-- Table: public.words

DROP TABLE IF EXISTS public.words;

DROP TYPE word_pair_status;
CREATE TYPE word_pair_status AS ENUM ('PENDING', 'OPEN', 'CLOSED');

CREATE TABLE IF NOT EXISTS public.words
(
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone,
    word1 character varying(24) COLLATE "C" NOT NULL,
    word2 character varying(24) COLLATE "C" NOT NULL,
    sem_similarity smallint CHECK (sem_similarity >= 0 AND sem_similarity <= 4),
    status word_pair_status DEFAULT 'PENDING'::word_pair_status,
    CONSTRAINT lex_order_check CHECK (word1::text < word2::text)
);
ALTER TABLE words ADD CONSTRAINT unique_word_pair UNIQUE(word1, word2);

INSERT INTO words (updated_at, word1, word2, sem_similarity) VALUES (CURRENT_TIMESTAMP,	'word1', 'word2', 0);

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.words
    OWNER to postgres;
