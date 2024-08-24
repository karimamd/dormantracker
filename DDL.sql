CREATE SCHEMA base;

CREATE TABLE base.tasks (
	id serial4 NOT NULL,
	date_added date NULL DEFAULT CURRENT_TIMESTAMP,
    created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    title varchar(150) NOT NULL,
	body text NULL,
	is_archived bool NULL DEFAULT false,
    category_id number
	CONSTRAINT tasks_pkey PRIMARY KEY (id)
);

CREATE TABLE base.categories (
	id serial4 NOT NULL,
	date_added date NULL DEFAULT CURRENT_TIMESTAMP,
    created_at timestamp NULL DEFAULT CURRENT_TIMESTAMP,
    title varchar(150) NOT NULL,
	body text NULL,
	is_archived bool NULL DEFAULT false,
	CONSTRAINT tasks_pkey PRIMARY KEY (id)
);