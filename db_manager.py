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
		    foreign key (user_id) references user(id)) engine INNODB;"""





