# from main.modules.jwt.controller import JWTController
from main.modules.log_event.model import LogEvent


class LogEventController:

    """
    UserController is used to handle all operations related to user.
    """

    @classmethod
    def log_event(cls , event_name, user_id, tid, path):
        info = {'event_name': event_name, 'user_id' : user_id, 'tid' : tid, 'path' : path}
        LogEvent.create(info)

    @classmethod
    def get_logs_for_tid_within_time_range(cls , tid, from_time, to_time):
        logs = LogEvent.query.filter(LogEvent.tid == tid, LogEvent.created_at >= from_time, LogEvent.created_at <= to_time).all()
        return [log.serialize() for log in logs]
