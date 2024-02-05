class Board:
    def __init__(self, board: list[list[str]]):
        self._board = board
        self._num_cols = len(board[0])
        self._num_rows = len(board)

    @staticmethod
    def create(board_str: str) -> 'Board':
        return Board(Board._parse_board_str(board_str))

    @staticmethod
    def _parse_board_str(board_str) -> list[list[str]]:
        symbol_to_word = {'C': 'computer', 'P': 'player', 'E': 'empty'}
        rows = board_str.split('|')
        board = [[symbol_to_word[cell] for cell in row] for row in rows]
        return board

    def get_num_player_moves(self):
        return self._count_coin('player')

    def get_num_computer_moves(self):
        return self._count_coin('computer')

    def drop_coin(self, col_idx: int, whose_move: str = 'player') -> None:
        for i in range(self._num_rows):
            if self._board[i][col_idx] == 'empty':
                self._board[i][col_idx] = whose_move
                return

    def get_next_available_column(self) -> int | None:
        for j in range(self._num_cols):
            for i in range(self._num_rows):
                if self._board[i][j] == 'empty':
                    return j
        return None

    def is_column_full(self, column_idx: int) -> bool:
        return self._board[-1][column_idx] != 'empty'

    def get_available_columns(self) -> list[int]:
        cols = []
        for j in range(self._num_cols):
            if not self.is_column_full(j):
                cols.append(j)
        return cols

    def get_winner(self):
        directions = [(1, 0), (0, 1), (1, 1), (1, -1)]

        for row in range(self._num_rows):
            for col in range(self._num_cols):
                for dx, dy in directions:
                    if self._check_winning_line(row, col, dx, dy):
                        return self._board[row][col]

        return None

    def _count_coin(self, whose: str):
        count = 0
        for row in self._board:
            for cell in row:
                if cell == whose:
                    count += 1
        return count

    def _check_winning_line(self, row, col, dx, dy):
        initial_cell = self._board[row][col]
        if initial_cell == 'empty':
            return False

        for i in range(1, 4):
            new_row = row + i * dx
            new_col = col + i * dy
            if new_row < 0 or new_row >= self._num_rows or new_col < 0 or new_col >= self._num_cols:
                return False
            if self._board[new_row][new_col] != initial_cell:
                return False

        return True
