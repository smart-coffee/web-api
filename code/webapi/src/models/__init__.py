from config import DB
import enum


SPORTSHALL_IMAGE_TABLE = DB.Table('sportshall_images', DB.Model.metadata,
                                  DB.Column('sportshall_id',
                                            DB.Integer,
                                            DB.ForeignKey('sportshall.id'),
                                            nullable=False),
                                  DB.Column('image_id',
                                            DB.Integer,
                                            DB.ForeignKey('image.id'),
                                            nullable=False))
TEAM_TRAININGSESSION_TABLE = DB.Table('team_trainingsessions', DB.Model.metadata,
                                      DB.Column('team_id',
                                                DB.Integer,
                                                DB.ForeignKey('team.id'),
                                                nullable=False),
                                      DB.Column('trainingsession_id',
                                                DB.Integer,
                                                DB.ForeignKey('trainingsession.id'),
                                                nullable=False))
NEWSENTRY_IMAGE_TABLE = DB.Table('newsentry_images', DB.Model.metadata,
                                  DB.Column('newsentry_id',
                                            DB.Integer,
                                            DB.ForeignKey('newsentry.id'),
                                            nullable=False),
                                  DB.Column('image_id',
                                            DB.Integer,
                                            DB.ForeignKey('image.id'),
                                            nullable=False))


class Weekday(DB.Model):
    __tablename__ = 'weekday'
    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(50), unique=True, nullable=False)
    ordinal = DB.Column(DB.Integer)

    def get_id(self):
        return self.id


class Club(DB.Model):
    __tablename__ = 'club'
    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(50), unique=True, nullable=False)

    # Foreign Keys #
    sportshall_id_fk = DB.Column(DB.Integer, DB.ForeignKey('sportshall.id', name='fk_club_sportshall'), nullable=False)

    # Relationships 1..n #
    teams = DB.relationship('Team', backref='club')
    roles = DB.relationship('ClubRole', backref='club')
    sessions = DB.relationship('TrainingSession', backref='club')
    news = DB.relationship('NewsEntry', back_populates='club')

    # Relationships n .. 1 #
    sportshall = DB.relationship('SportsHall', foreign_keys=[sportshall_id_fk])

    def get_id(self):
        return self.id


class Team(DB.Model):
    __tablename__ = 'team'

    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    numbering = DB.Column(DB.Integer)
    name = DB.Column(DB.String(50), unique=True)

    # Foreign Keys #
    club_id_fk = DB.Column(DB.Integer, DB.ForeignKey('club.id', name='fk_team_club'), nullable=False)
    # leader_id_fk = DB.Column(DB.Integer, DB.ForeignKey('player.id'))
    leader_id_fk = DB.Column(DB.Integer, DB.ForeignKey('player.id', use_alter=True, name='fk_team_leader'))

    # Relationships n .. 1 #
    leader = DB.relationship('Player', foreign_keys=[leader_id_fk])

    # Relationships n .. m #
    sessions = DB.relationship('TrainingSession', secondary=TEAM_TRAININGSESSION_TABLE, back_populates='teams')

    def get_id(self):
        return self.id


class Player(DB.Model):
    __tablename__ = 'player'

    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    public_id = DB.Column(DB.String(100), unique=True, nullable=False)
    first_name = DB.Column(DB.String(50), nullable=False)
    last_name = DB.Column(DB.String(50), nullable=False)
    position = DB.Column(DB.Integer)

    # Foreign keys #
    team_id_fk = DB.Column(DB.Integer, DB.ForeignKey('team.id', name='fk_player_team'))
    image_id_fk = DB.Column(DB.Integer, DB.ForeignKey('image.id', name='fk_player_image'), nullable=False)

    # Relationships 1 .. n #
    information = DB.relationship('Information', backref='player')
    roles = DB.relationship('ClubRole', backref='player')

    # Relationships n .. 1 #
    team = DB.relationship('Team', foreign_keys=[team_id_fk], backref='members')
    image = DB.relationship('Image', foreign_keys=[image_id_fk])

    def get_id(self):
        return self.public_id


class Image(DB.Model):
    __tablename__ = 'image'

    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    path = DB.Column(DB.String(200), nullable=False)
    title = DB.Column(DB.String(50), nullable=False)

    def get_id(self):
        return self.id


class InformationType(enum.Enum):
    CONTACT = 1
    PLAYER = 2
    OTHERS = 3


class Information(DB.Model):
    __tablename__ = 'information'

    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    attribute = DB.Column(DB.String(50), nullable=False)
    val = DB.Column(DB.String(50), nullable=False)
    type = DB.Column(DB.Enum(InformationType), nullable=False)

    # Foreign Keys #
    # Information about a player, backref is ON
    player_id_fk = DB.Column(DB.Integer, DB.ForeignKey('player.id', name='fk_information_player'), nullable=False)

    def get_id(self):
        return self.id


class SportsHall(DB.Model):
    __tablename__ = 'sportshall'

    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    street = DB.Column(DB.String(50), nullable=False)
    street_number = DB.Column(DB.Integer, nullable=False)
    zip_code = DB.Column(DB.String(20), nullable=False)
    place = DB.Column(DB.String(20), nullable=False)
    country = DB.Column(DB.String(50), nullable=False)
    state = DB.Column(DB.String(50), nullable=False)

    # Relationships n .. m #
    images = DB.relationship('Image', secondary=SPORTSHALL_IMAGE_TABLE)

    def get_id(self):
        return self.id


class ClubRole(DB.Model):
    __tablename__ = 'clubrole'

    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(50), nullable=False)

    # Foreign Keys #
    # Responsible player, backref is ON
    player_id_fk = DB.Column(DB.Integer, DB.ForeignKey('player.id', name='fk_clubrole_player'))
    # belonging club, backref is ON
    club_id_fk = DB.Column(DB.Integer, DB.ForeignKey('club.id', name='fk_clubrole_club'), nullable=False)

    def get_id(self):
        return self.id


class TrainingSession(DB.Model):
    __tablename__ = 'trainingsession'

    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    start_hour = DB.Column(DB.Integer, nullable=False)
    start_minute = DB.Column(DB.Integer, nullable=False)
    end_hour = DB.Column(DB.Integer, nullable=False)
    end_minute = DB.Column(DB.Integer, nullable=False)

    # Foreign Keys #
    club_id_fk = DB.Column(DB.Integer, DB.ForeignKey('club.id', name='fk_trainingsession_club'), nullable=False)
    day_id_fk = DB.Column(DB.Integer, DB.ForeignKey('weekday.id', name='fk_trainingsession_weekday'), nullable=False)

    # Relationships n .. 1 #
    day = DB.relationship('Weekday', foreign_keys=[day_id_fk])

    # Relationships n .. m #
    teams = DB.relationship('Team', secondary=TEAM_TRAININGSESSION_TABLE, back_populates='sessions')

    def get_id(self):
        return self.id


class Topic(DB.Model):
    __tablename__ = 'topic'

    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(50), nullable=False, unique=True)

    # Relationships 1 .. n
    entries = DB.relationship('NewsEntry', back_populates='topic')


class Author(DB.Model):
    __tablename__ = 'author'

    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    name = DB.Column(DB.String(50), nullable=False, unique=True)
    shorthand_symbol = DB.Column(DB.String(50), nullable=False, unique=True)

    # Relationships 1 .. n
    entries = DB.relationship('NewsEntry', back_populates='author')


class NewsEntry(DB.Model):
    __tablename__ = 'newsentry'

    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    title = DB.Column(DB.String(100), nullable=False)
    description = DB.Column(DB.Text, nullable=False)
    publish_date = DB.Column(DB.DateTime, nullable=False)
    view_count = DB.Column(DB.Integer, nullable=False, server_default=DB.text('0'))

    # Foreign Keys #
    topic_id_fk = DB.Column(DB.Integer, DB.ForeignKey('topic.id', name='fk_newsentry_topic'), nullable=False)
    author_id_fk = DB.Column(DB.Integer, DB.ForeignKey('author.id', name='fk_newsentry_author'), nullable=False)
    club_id_fk = DB.Column(DB.Integer, DB.ForeignKey('club.id', name='fk_newsentry_club'), nullable=False)
    preview_image_id_fk = DB.Column(DB.Integer, DB.ForeignKey('image.id', name='fk_newsentry_previewimage'))

    # Relationships n .. 1
    topic = DB.relationship('Topic', foreign_keys=[topic_id_fk], back_populates='entries')
    author = DB.relationship('Author', foreign_keys=[author_id_fk], back_populates='entries')
    club = DB.relationship('Club', foreign_keys=[club_id_fk], back_populates='news')
    preview_image = DB.relationship('Image', foreign_keys=[preview_image_id_fk])

    # Relationships n .. m
    images = DB.relationship('Image', secondary=NEWSENTRY_IMAGE_TABLE)


class User(DB.Model):
    __tablename__ = 'user'

    # Attributes #
    id = DB.Column(DB.Integer, primary_key=True)
    public_id = DB.Column(DB.String(100), unique=True, nullable=False)
    password = DB.Column(DB.String(100), nullable=False)
    name = DB.Column(DB.String(50), nullable=False, unique=True)
    email = DB.Column(DB.String(50), nullable=False, unique=True)
