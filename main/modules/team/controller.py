from main.modules.jwt.controller import JWTController
from main.modules.team.model import Team
from main.modules.log_event.controller import LogEventController


class TeamController:
    """
    TeamController is used to handle all operations related to team.
    """

    @classmethod
    def get_teams(cls) -> list[dict]:
        """
        To get all the teams
        :return:
        """
        teams = Team.query.all()
        LogEventController.log_event("get_teams" , "admin" , "NONE")
        return [team.serialize() for team in teams]

    @classmethod
    def get_team(cls , tid) -> dict:
        """"
        To get the team from tid
        """

        team = Team.query.filter_by(tid=tid).first()
        team = team.serialize()
        user_id = JWTController.get_user_identity()["user_id"]
        LogEventController.log_event("get_team" , user_id , tid , "team/getTeam/<string:tid>")
        return team

    @classmethod
    def create_team_profile(cls , data):

        LogEventController.log_event("create_team" , "ADMIN" , "ADMIN", "/team/create")
        Team.create(data)
