from flask_restful import fields

from config import SWAG


@SWAG.definition('User')
def get_registered_user_details():
    """
    file: /controllers/response_model/user.yml
    """
    _user_fields = {
        'public_id': fields.String,
        'name': fields.String,
        'email': fields.String
    }
    return _user_fields


@SWAG.definition('Role')
def get_role_fields():
    """
    file: /controllers/response_model/role.yml
    """
    _role_fields = {
        'id': fields.Integer,
        'name': fields.String
    }
    return _role_fields


@SWAG.definition('CoffeeMachine')
def get_coffee_machine_fields():
    """
    file: /controllers/response_model/coffee_machine.yml
    """
    _coffee_machine_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'repository': fields.String
    }
    return _coffee_machine_fields


@SWAG.definition('Image')
def get_image_fields():
    """
    file: /controllers/response_model/image.yml
    """
    _image_fields = {
        'id': fields.Integer,
        'path': fields.String,
        'title': fields.String
    }
    return _image_fields


@SWAG.definition('SportsHall')
def get_sportshall_fields():
    """
    file: /controllers/response_model/sportshall.yml
    """
    _sportshall_fields = {
        'id': fields.Integer,
        'street': fields.String,
        'street_number': fields.Integer,
        'zip_code': fields.String,
        'place': fields.String,
        'country': fields.String,
        'state': fields.String,
        'has_images': fields.Boolean
        # 'images': fields.List(fields.Nested(get_image_fields()))
    }
    return _sportshall_fields


@SWAG.definition('Team')
def get_team_fields():
    """
    file: /controllers/response_model/team.yml
    """
    _team_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'numbering': fields.Integer,
        'leader_id': fields.String,
        'has_players': fields.Boolean
    }
    return _team_fields


@SWAG.definition('Player')
def get_player_fields():
    """
    file: /controllers/response_model/player.yml
    """
    _player_fields = {
        'public_id': fields.String,
        'first_name': fields.String,
        'last_name': fields.String,
        'team_id': fields.Integer,
        'position': fields.Integer,
        'has_information': fields.Boolean,
        'image': fields.Nested(get_image_fields())
    }
    return _player_fields


@SWAG.definition('Information')
def get_information_fields():
    """
    file: /controllers/response_model/information.yml
    """
    _information_fields = {
        'attribute': fields.String,
        'val': fields.String
    }
    return _information_fields


@SWAG.definition('TrainingSession')
def get_training_session_fields():
    """
    file: /controllers/response_model/trainingsession.yml
    """
    _training_session_fields = {
        'id': fields.Integer,
        'start_hour': fields.Integer,
        'start_minute': fields.Integer,
        'end_hour': fields.Integer,
        'end_minute': fields.Integer,
        'weekday_id': fields.Integer
    }
    return _training_session_fields


@SWAG.definition('Weekday')
def get_weekday_fields():
    """
    file: /controllers/response_model/trainingsession.yml
    """
    _weekday_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'ordinal': fields.Integer
    }
    return _weekday_fields


@SWAG.definition('Author')
def get_author_fields():
    """
    file: /controllers/response_model/author.yml
    """
    _author_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'shorthand_symbol': fields.String
    }
    return _author_fields


@SWAG.definition('Topic')
def get_topic_fields():
    """
    file: /controllers/response_model/topic.yml
    """
    _topic_fields = {
        'id': fields.Integer,
        'name': fields.String
    }
    return _topic_fields


@SWAG.definition('NewsEntry')
def get_news_fields():
    """
    file: /controllers/response_model/newsentry.yml
    """
    _news_entry_fields = {
        'id': fields.Integer,
        'title': fields.String,
        'description': fields.String,
        'publish_date': fields.DateTime,
        'topic': fields.Nested(get_topic_fields()),
        'author': fields.Nested(get_author_fields()),
        'club_id': fields.Integer,
        'has_images': fields.Boolean,
        'view_count': fields.Integer
    }
    return _news_entry_fields


@SWAG.definition('NewsEntryPreview')
def get_news_preview_fields():
    """
    file: /controllers/response_model/newsentrypreview.yml
    """
    _news_entry_preview_fields = {
        'id': fields.Integer,
        'title': fields.String,
        'publish_date': fields.DateTime,
        'topic': fields.Nested(get_topic_fields()),
        'author': fields.Nested(get_author_fields()),
        'club_id': fields.Integer,
        'has_preview_image': fields.Boolean,
        'view_count': fields.Integer
    }
    return _news_entry_preview_fields


@SWAG.definition('Token')
def get_token_fields():
    """
    file: /controllers/response_model/token.yml
    """
    _token_fields = {
        'token': fields.String
    }
    return _token_fields


@SWAG.definition('ClubRole')
def get_club_role_fields():
    """
    file: /controllers/response_model/club_role.yml
    """
    _club_role_fields = {
        'id': fields.Integer,
        'name': fields.String,
        'club_id': fields.Integer,
        'player_id': fields.String,
    }
    return _club_role_fields
