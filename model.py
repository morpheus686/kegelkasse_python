from database import Database
from database_access import SumPerPlayerViewAccess


class MainWindowModel:
    def __init__(self, db_name: str):
        self.database = Database(db_name)
        self.viewAccess = SumPerPlayerViewAccess(self.database)

    def get_all_player_penalties(self):
        return self.viewAccess.get_all()

