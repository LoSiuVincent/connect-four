class Board:
    def __init__(self, board: list[list[str]]):
        self._board = board
        self._num_cols = len(board[0])
        self._num_rows = len(board)

    @staticmethod
    def create(board_str: str):
        return Board(Board._parse_board_str(board_str))

    @staticmethod
    def _parse_board_str(board_str):
        symbol_to_word = {'C': 'computer', 'P': 'player', 'E': 'empty'}
        rows = board_str.split('|')
        board = [[symbol_to_word[cell] for cell in row] for row in rows]
        return board

    def get_next_available_column(self):
        for j in range(self._num_cols):
            for i in range(self._num_rows):
                if self._board[i][j] == 'empty':
                    return j
        return None
