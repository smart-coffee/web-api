from config.flask_config import ResourceNotFound
from models import NewsEntry, Club, TrainingSession, Player, SportsHall, Team, ClubRole, User


def run_training_session_fixture(session: TrainingSession):
    session.weekday_id = session.day.id


def run_player_fixture(player: Player):
    player.team_id = player.team_id_fk
    player.has_information = True if player.information else False


def run_sportshall_fixture(sportshall: SportsHall):
    sportshall.has_images = True if sportshall.images else False


def run_team_fixture(team: Team):
    if not team.leader:
        # Should raise exception, because a team should always have a leader
        raise ResourceNotFound('Team has no leader')
    team.leader_id = team.leader.public_id

    team.has_players = True if team.members else False

    if not team.name:
        _club_name = team.club.name
        team.name = '{0} {1}'.format(_club_name, team.numbering)

    run_player_fixture(team.leader)

    for player in team.members:
        run_player_fixture(player)

    for session in team.sessions:
        run_training_session_fixture(session)


def run_news_entry_fixture(news_entry: NewsEntry):
    news_entry.club_id = news_entry.club_id_fk
    news_entry.has_images = True if news_entry.images else False
    news_entry.has_preview_image = True if news_entry.preview_image else False


def run_club_role_fixture(club_role: ClubRole):
    club_role.club_id = club_role.club_id_fk
    club_role.player_id = club_role.player.public_id


def run_club_fixture(club: Club):
    for news in club.news:
        run_news_entry_fixture(news)

    for session in club.sessions:
        run_training_session_fixture(session)

    for team in club.teams:
        run_team_fixture(team)

    run_sportshall_fixture(club.sportshall)

    for role in club.roles:
        run_club_role_fixture(role)


def run_user_fixture(user: User):
    pass
