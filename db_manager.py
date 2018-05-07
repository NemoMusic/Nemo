import pymysql

connection = None

connection = pymysql.connect(host='nemo.cnj8noexhne9.eu-west-1.rds.amazonaws.com',
                            user='nemo',
                            password='nemoadmin',
                            db='nemodb')


def execute_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    return cursor.fetchone()


def test_connection():
    result = execute_sql("SELECT VERSION()")
    if result:
        return True
    else:
        return False


create_user_table = """create table user(
            id             int not null auto_increment,
            email          varchar(50) not null unique,
            name           varchar(20) not null,
            last_name      varchar(20) not null,
            gender         varchar(10),
            user_name      varchar(20) not null unique,
            password       varchar(20) not null,
            wallet         numeric(8,2),
            birth_date	   date,
            primary key (id)) engine = INNODB;"""


create_event_table="""create table event(
            id          varchar(10) not null auto_increment,
            name		varchar(50) not null,
            date        date not null,
            location    varchar(50) not null,
            about       varchar(140),
            primary key (id)) engine = INNODB;"""


create_artist_table = """create table artist(
		    user_id                     int  primary key,
		    account_validation_date     date,
		    primary key (user_id),
		    foreign key (user_id) references user(id)) engine = INNODB;"""


create_playlist_table ="""create table playlist(
            id              varchar(10)  not null auto_increment,
            title           varchar(20) not null,
            create_date     date(20),
            is_private      varchar(10) not null,
            user_id         varchar(20) not null,
            primary key (id),
            foreign key (user_id) references user(id)) engine = INNODB;"""


create_album_table="""create table album(
            id		        varchar(10)  not null auto_increment,
            title			varchar(20) not null,
            release_date	date(20),
            price			int not null,
            primary key (id)) engine = INNODB;"""


create_song_table = """create table song(
            id			    varchar(10)  not null auto_increment,
            title			varchar(20) not null,
            release_date	date(20) not null,
            duration		time(5) not null,
            number_of_listen	int,
            price			int,
            album_id		varchar(10) not null,
            primary key (id),
            foreign key (album_id) references album(id))engine = INNODB;"""


create_genre_table = """create table genre(
		    name     varchar(10) not null,
		    primary key (name))engine = INNODB;"""


create_activity_table = """create table activity(
            id			    varchar(10) not null auto_increment,
            date			date(10) not null,
            entitiy_type	varchar(5) not null,
            action_type		varchar(5) not null,
            user_id 		varchar(10) not null,
            primary key (id),
            foreign key (user_id) references user(id))engine = INNODB;"""


create_share_table = """create table share(
            activity_id			varchar(10) not null,
            share_comment		varchar(50),
            foreign key (activity_id) references activity(id))engine = INNODB;"""

create_follow_table ="""create table follow(
            activity_id int NOT NULL,
            FOREIGN KEY (activity_id) REFERENCES activity(id),
            PRIMARY KEY (activity_id)
) engine = INNODB;"""

create_rate_table ="""create table rate(
            activity_id int NOT NULL,
            value int NOT NULL,
            FOREIGN KEY (activity_id) REFERENCES album(id),
            PRIMARY KEY (activity_id)
) engine = INNODB;"""

create_comment_table ="""create table comment(
            activity_id int NOT NULL,
            text  VARCHAR(50) NOT NULL,
            FOREIGN KEY (activity_id) REFERENCES album(id),
            PRIMARY KEY (activity_id)
) engine = INNODB;"""
