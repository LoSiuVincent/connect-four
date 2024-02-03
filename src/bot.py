class Bot:
    def __init__(self, strategy: str):
        self._strategy = strategy

    def predict(self, board_str: str):
        if self._strategy == 'fixed':
            pass
