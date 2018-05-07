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


create_follow_table = """create table follow(
		activity_id int not null ,
		primary key (activity_id),
		foreign key (activity_id) references activity(id))engine = INNODB;"""



create_user_follow = """create table user_follow(
            follower_id  int not null,
            following_id  int not null,
            primary key (follower_id, following_id ),
            foreign key follower_id references User(ID)
            on delete cascade on update cascade,
            foreign key following_id references User(ID) 
            on delete cascade on update cascade);"""

create_user_song = """create table user_song(
            user_id   int not null,
            song_id   int not null,
            primary key (follower_id, following_id ),
            foreign key user_id references User(ID)
            on delete cascade on update cascade,
            foreign key song_id references Song(ID)
            on delete cascade on update cascade);"""

create_user_album = """create table user_album(
            user_id       int not null,
            album_id      int not null,
            primary key (user_id, album_id ),
            foreign key user_id references User(id)
            on delete cascade on update cascade,
            foreign key album_id references Album(id)
            on delete cascade on update cascade);"""

create_artist_song = """create table artist_song(
            user_id  int not null,
            song_id  int not null,
            primary key (user_id, album_id ),
            foreign key user_id references Artist(user_id)
            on delete cascade on update cascade,
            foreign key album_id references Album(id)
            on delete cascade on update cascade);"""

create_participation = """create table participation(
            user_id       varchar(10) not null,
            artist_id     varchar(10) not null,
            event_id      varchar(10),
            primary key (user_id,artist_id,event_id),
            foreign key(user_id) references User(id)
            on delete cascade on update cascade,
            foreign key(artist_id) references Artist(user_id)
            on delete cascade on update cascade,
            foreign key(event_id) references Event(id)
            on delete cascade on update cascade);"""

create_playlist_song = """create table playlist_song(
            song_id       varchar(10) not null,
            playlist_id   varchar(10) not null,
            primary key (song_id, playlist_id),
            foreign key(song_id) references Song(id)
            on delete cascade on update cascade,
            foreign key(playlist_id) references Playlist(id)
            on delete cascade on update cascade);"""

create_comment_reply = """create table comment_reply(
            reply_id    varchar(10) not null,
            parent_id   varchar(10) not null,
            primary key (reply_id),
            foreign key(parent_id) references Comment(activity_id)
            on delete cascade on update cascade);"""

create_table_song_genre = """create table song_genre(
            song_id     varchar(10) not null,
            genre_name  varchar(10) not null,
            primary key (song_id, genre_name),
            foreign key(song_id) references Song(id)
            on delete cascade on update cascade,
            foreign key(genre_name) references Genre(name)
            on delete cascade on update cascade);"""