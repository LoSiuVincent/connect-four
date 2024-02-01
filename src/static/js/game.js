export class Game {
	constructor() {
		this.board = make2DBoard(6, 7);
	}

	getCellState(row, col) {
		return this.board[row][col];
	}

	dropCoin(colIndex, whoseMove) {
		whoseMove = (whoseMove === undefined) ? "player" : whoseMove;
		for (let i = 0; i < 6; i++) {
			if (this.board[i][colIndex] === "empty") {
				this.board[i][colIndex] = whoseMove;
				break;
			}
		}
	}

	getWinner() {
		const directions = [
			{ x: 1, y: 0 },
			{ x: 0, y: 1 },
			{ x: 1, y: 1 },
			{ x: 1, y: -1 }
		];

		for (let row = 0; row < this.board.length; row++) {
			for (let col = 0; col < this.board[row].length; col++) {
				for (const direction of directions) {
					if (this._checkWinningLine(row, col, direction.x, direction.y)) {
						return this.board[row][col];
					}
				}
			}
		}

		return "";
	}

	_checkWinningLine(row, col, dx, dy) {
		const initialCell = this.board[row][col];
		if (initialCell === "empty") return false;

		for (let i = 1; i < 4; i++) {
			const newRow = row + i * dx;
			const newCol = col + i * dy;
			if (newRow < 0 || newRow >= this.board.length || newCol < 0 || newCol >= this.board[row].length) {
				return false;
			}
			if (this.board[newRow][newCol] !== initialCell) {
				return false;
			}
		}
		return true;
	}
}

export function make2DBoard(rows, cols) {
	let board = [];
	for (let i = 0; i < rows; i++) {
		board[i] = [];
		for (let j = 0; j < cols; j++) {
			board[i][j] = "empty";
		}
	}
	return board;
}
