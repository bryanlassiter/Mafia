create table if not exists users  (
	id integer not null primary key autoincrement,
	firstName string not null,
	lastName string not null,
	userName string not null,
	hashedPassword string not null,
	isAdmin boolean not null
);
drop table if exists games;
create table games (
	id integer primary key autoincrement,
	dayNight integer not null,
	dateCreated date not null,
	time decimal
);

drop table if exists players;
create table players (
	id integer not null primary key autoincrement,
	isDead boolean not null,
    lat decimal not null,
    lng decimal not null,
	userID integer not null,
	isWerewolf boolean not null
);

create table if not exists kills (
	killerID integer not null,
	victimID integer not null,
	timestamp timestamp not null,
	lat decimal not null,
	lng decimal not null
);
