drop table if exists users;
create table users (
	id integer primary key autoincrement,
	firstName string not null,
	lastName string not null,
	userName string not null,
	hashedPassword string not null,
	isAdmin string not null
);
