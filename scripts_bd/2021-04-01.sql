CREATE TABLE db.movies (
	id BIGINT UNSIGNED auto_increment NOT NULL,
	title varchar(100) NOT NULL,
	isan varchar(100) NOT NULL,
	trailer_url varchar(200) NULL,
	duration SMALLINT UNSIGNED NOT NULL COMMENT 'in minutes',
	release_year SMALLINT UNSIGNED NULL,
	CONSTRAINT movies_UN UNIQUE KEY (isan),
	CONSTRAINT movies_PK PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;

CREATE TABLE db.genres (
	id BIGINT UNSIGNED auto_increment NOT NULL,
	name varchar(30) NOT NULL,
	CONSTRAINT genres_PK PRIMARY KEY (id)
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;

CREATE TABLE db.movies_genres (
	id BIGINT UNSIGNED auto_increment NOT NULL,
	movie_id BIGINT UNSIGNED NOT NULL,
	genre_id BIGINT UNSIGNED NOT NULL,
	CONSTRAINT movies_genres_UN UNIQUE KEY (movie_id,genre_id),
	CONSTRAINT movies_genres_PK PRIMARY KEY (id),
	CONSTRAINT movies_genres_FK FOREIGN KEY (movie_id) REFERENCES db.movies(id) ON DELETE RESTRICT ON UPDATE CASCADE,
	CONSTRAINT movies_genres_FK_1 FOREIGN KEY (genre_id) REFERENCES db.genres(id) ON DELETE RESTRICT ON UPDATE CASCADE
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;

CREATE TABLE db.movies_rating (
	id BIGINT UNSIGNED auto_increment NOT NULL,
	movie_id BIGINT UNSIGNED NOT NULL,
	rating SMALLINT UNSIGNED NOT NULL COMMENT '0-10',
	CONSTRAINT movies_rating_PK PRIMARY KEY (id),
	CONSTRAINT movies_rating_FK FOREIGN KEY (movie_id) REFERENCES db.movies(id) ON DELETE RESTRICT ON UPDATE CASCADE
)
ENGINE=InnoDB
DEFAULT CHARSET=utf8
COLLATE=utf8_general_ci;
