CREATE TABLE

    `tasks` (
        `id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `status` INT(11) NOT NULL,
        `user_id` INT(11),
        `id_parent` INT(11),
        FOREIGN KEY (user_id) REFERENCES users(id)

    );

CREATE TABLE

	`users` (
		`id` INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,
        `name` CHAR(30) NOT NULL
	);