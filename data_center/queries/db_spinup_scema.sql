--show data_directory; #postgres data dir
--show all;            #general postgres info


--add gross sales, revanue, 

create database db_v1;
\connect db_v1;
create schema  data_center
	--table of users
	create table data_center.users_tbl(
		user_id         serial      not null PRIMARY KEY,
		first_name      text        not null,
		last_name       text        not null,
		user_name       text        not null,
		password        text        not null,
		email           text        not null unique,
		sign_up_date    timestamp   not null default current_timestamp
	)

	--table of messages user post (mapped to users and htags to msg tables)
	create table data_center.user_activation_tbl(
		user_id         integer     not null PRIMARY KEY,
		activation_code text        not null unique,
		activated       boolean     not null default false,
		FOREIGN KEY    (user_id)    REFERENCES data_center.users_tbl (user_id)
	)

	--table of messages user post (mapped to users and htags to msg tables)
	create table data_center.user_reviews(
		review_id       bigserial   not null PRIMARY KEY,
		user_id         integer     not null REFERENCES data_center.users_tbl (user_id),
		reviewer_id     integer     not null REFERENCES data_center.users_tbl (user_id),
		review_text     text        not null,
		overall_rating  smallint    not null default 0
	)

	--table of messages user post (mapped to users and htags to msg tables)
	create table data_center.user_location_tbl(
		user_id         integer     not null PRIMARY KEY,
		latitude        integer     not null,
		longitude       integer     not null
	)

	--table of all users to their last viewed post
	create table data_center.last_viewed(
		user_id   integer     not null PRIMARY KEY,
		idea_id   bigint      not null
	)

	-- table of categories to their id
	create table data_center.categories(
		--id        serial not null primary key,
		ctree     jsonb
	)

	-- table of user locations (updated frequently and same size as users table)
	create table data_center.users_ideas_tbl(
		idea_id      bigserial  not null PRIMARY KEY,
		user_id      integer    not null,
		winner_id    integer            ,
		views        integer            ,
		title        text       not null,
		summary      text       not null,
		category     smallint   not null,
		existing     boolean    not null default false, -- whether idea has cultivated in a business that has started
		partners     smallint   not null default 0,     -- number of acceptable partners; default of 0 == any
		post_date    timestamp  not null default current_timestamp,
		end_date     timestamp  not null default current_timestamp
	);