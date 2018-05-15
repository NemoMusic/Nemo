import pymysql
from db_methods import follow,playlist
connection = None

connection = pymysql.connect(host='nemo.cnj8noexhne9.eu-west-1.rds.amazonaws.com',
                             user='nemo',
                             password='nemoadmin',
                             db='nemodb')


def execute_sql(sql):
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.commit()
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

create_event_table = """create table event(
            id          int not null auto_increment,
            name		varchar(50) not null,
            date        date not null,
            location    varchar(50) not null,
            about       varchar(140),
            primary key (id)) engine = INNODB;"""

create_artist_table = """create table artist(
		    user_id                     int ,
		    account_validation_date     date,
		    primary key (user_id),
		    foreign key (user_id) references user(id)) engine = INNODB;"""

create_playlist_table = """create table playlist(
            id              int  not null auto_increment,
            title           varchar(20) not null,
            create_date     date,
            is_private      varchar(10) not null,
            user_id         int not null,
            primary key (id),
            foreign key (user_id) references user(id)) engine = INNODB;"""

create_album_table = """create table album(
            id		        int  not null auto_increment,
            title			varchar(20) not null,
            release_date	date,
            price			int not null,
            primary key (id)) engine = INNODB;"""

create_song_table = """create table song(
            id			    int  not null auto_increment,
            title			varchar(20) not null,
            release_date	date not null,
            duration		time(5) not null,
            number_of_listen	int,
            price			int,
            album_id		int not null,
            primary key (id),
            foreign key (album_id) references album(id))engine = INNODB;"""

create_genre_table = """create table genre(
		    name     varchar(10) not null,
		    primary key (name))engine = INNODB;"""

create_activity_table = """create table activity(
            id			    int not null auto_increment,
            date			date not null,
            entitiy_type	varchar(5) not null,
            action_type		varchar(5) not null,
            user_id 		int not null,
            primary key (id),
            foreign key (user_id) references user(id))engine = INNODB;"""

create_share_table = """create table share(
            activity_id			int not null,
            share_comment		varchar(50),
            primary key (activity_id),
            foreign key (activity_id) references activity(id))engine = INNODB;"""

create_follow_table = """create table follow(
            activity_id int NOT NULL,
            FOREIGN KEY (activity_id) REFERENCES activity(id),
            PRIMARY KEY (activity_id)
) engine = INNODB;"""

create_rate_table = """create table rate(
            activity_id int NOT NULL,
            value int NOT NULL,
            FOREIGN KEY (activity_id) REFERENCES album(id),
            PRIMARY KEY (activity_id)
) engine = INNODB;"""

create_comment_table = """create table comment(
            activity_id int NOT NULL,
            text  VARCHAR(50) NOT NULL,
            FOREIGN KEY (activity_id) REFERENCES album(id),
            PRIMARY KEY (activity_id)
) engine = INNODB;"""

create_user_follow = """create table user_follow(
            follower_id   int not null,
            following_id  int not null,
            primary key (follower_id, following_id ),
            foreign key(follower_id) references user(id)
            on delete cascade on update cascade,
            foreign key(following_id) references user(id) 
            on delete cascade on update cascade) engine = INNODB;"""

create_user_song = """create table user_song(
            user_id   int not null,
            song_id   int not null,
            primary key (user_id,song_id),
            foreign key(user_id) references user(id)
            on delete cascade on update cascade,
            foreign key(song_id) references song(id)
            on delete cascade on update cascade) engine = INNODB;"""

create_user_album = """create table user_album(
            user_id       int not null,
            album_id      int not null,
            primary key (user_id, album_id ),
            foreign key(user_id) references user(id)
            on delete cascade on update cascade,
            foreign key(album_id) references album(id)
            on delete cascade on update cascade) engine = INNODB;"""

create_artist_song = """create table artist_song(
            user_id  int not null,
            song_id  int not null,
            primary key (user_id,song_id),
            foreign key(user_id) references artist(user_id)
            on delete cascade on update cascade,
            foreign key(song_id) references song(id)
            on delete cascade on update cascade) engine = INNODB;"""
'''
create_participation = """create table participation(
            user_id       int not null,
            artist_id     int not null,
            event_id      int,
            primary key (user_id,artist_id,event_id),
            foreign key(user_id) references user(id)
            on delete cascade on update cascade,
            foreign key(artist_id) references artist(user_id)
            on delete cascade on update cascade,
            foreign key(event_id) references event(id)
            on delete cascade on update cascade) engine = INNODB;"""
'''
create_participation_user = """ create table participation_user(
            user_id       int not null,
            event_id      int not null,
            primary key(user_id,event_id),
            foreign key(user_id) references user(id)
            on delete cascade on update cascade,
            foreign key(event_id) references event(id)
            on delete cascade on update cascade) engine = INNODB;"""
create_participation_artist = """create table participation_artist(
            artist_id       int not null,
            event_id      int not null,
            primary key(artist_id,event_id),
            foreign key(artist_id) references artist(user_id)
            on delete cascade on update cascade,
            foreign key(event_id) references event(id)
            on delete cascade on update cascade) engine = INNODB;"""

create_playlist_song = """create table playlist_song(
            song_id       int not null,
            playlist_id   int not null,
            primary key (song_id, playlist_id),
            foreign key(song_id) references song(id)
            on delete cascade on update cascade,
            foreign key(playlist_id) references playlist(id)
            on delete cascade on update cascade) engine = INNODB;"""

create_comment_reply = """create table comment_reply(
            reply_id    int not null,
            parent_id   int not null,
            primary key (reply_id),
            foreign key(parent_id) references comment(activity_id)
            on delete cascade on update cascade) engine = INNODB;"""

create_table_song_genre = """create table song_genre(
            song_id     int not null,
            genre_name  varchar(10) not null,
            primary key (song_id, genre_name),
            foreign key(song_id) references song(id)
            on delete cascade on update cascade,
            foreign key(genre_name) references genre(name)
            on delete cascade on update cascade) engine = INNODB;"""

create_view_song_rate = """create view song_rate as 
            SELECT s.id as song_id, avg(r.value) as rate
            FROM song s join activity a join rate r
            WHERE a.action_type = 'RATE' and a.entity_type = 'SONG' and r.activity_id = a.id and a.entity_id = s.id
            GROUP BY s.id"""

create_view_album_rate = """create view album_rate as
            SELECT a.id album_id, avg(r.value) as rate
            FROM album a join activity ac join rate r
            WHERE ac.action_type = 'RATE' and ac.entity_type = 'ALBUM' and r.activity_id = a.id and ac.entity_id = a.id
            GROUP BY a.id"""


create_view_following_playlists = """create view following_playlist as
          SELECT pl.*
          FROM activity a, user u, playlist pl
          WHERE(a.user_id = u.id AND a.action_type = '%s' AND a.entity_type = '%s')
""" % (follow,playlist)


create_user_index ="""create index uname on user(user_name)"""

#execute_sql(create_view_following_playlists)
#execute_sql(create_user_index)
# execute_sql(create_view_album_rate)
# execute_sql(create_view_song_rate)
# execute_sql(create_user_table)
# execute_sql(create_event_table)
# execute_sql(create_artist_table)
# execute_sql(create_playlist_table)
# execute_sql(create_album_table)
# execute_sql(create_song_table)
# execute_sql(create_genre_table)
# execute_sql(create_activity_table)
# execute_sql(create_share_table)
# execute_sql(create_follow_table)
# execute_sql(create_rate_table)
# execute_sql(create_comment_table)
# execute_sql(create_user_follow)
# execute_sql(create_user_song)
# execute_sql(create_user_album)
# execute_sql(create_artist_song)
# execute_sql(create_playlist_song)
# execute_sql(create_comment_reply)
# execute_sql(create_table_song_genre)
# execute_sql(create_participation_artist)
# execute_sql(create_participation_user)
