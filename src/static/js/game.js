export class Game {
	constructor() {
		this.board = make2DBoard(6, 7);
	}

	getCellState(col, row) {
		return this.board[row][col];
	}

	dropCoin(colIndex) {
		for (let i = 0; i < 6; i++) {
			if (this.board[i][colIndex] === "empty") {
				this.board[i][colIndex] = "player";
				break;
			}
		}
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
