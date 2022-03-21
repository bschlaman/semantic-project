-- Table: public.words

-- DROP TABLE IF EXISTS public.words;

CREATE TABLE IF NOT EXISTS public.words
(
    id uuid NOT NULL DEFAULT gen_random_uuid(),
    created_at timestamp without time zone NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at timestamp without time zone,
    word1 character varying(24) COLLATE pg_catalog."default" NOT NULL,
    word2 character varying(24) COLLATE pg_catalog."default" NOT NULL,
    similarity int4range,
    status character varying(10) COLLATE pg_catalog."default" NOT NULL DEFAULT 'PENDING'::character varying,
    CONSTRAINT words_pkey PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.words
    OWNER to postgres;
