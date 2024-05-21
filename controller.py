from model import MainWindowModel


class MainWindowController:
    def __init__(self, model: MainWindowModel, view):
        self.view = view
        self.model = model

    def update_view(self):
        all_penalties = self.model.get_all_player_penalties()