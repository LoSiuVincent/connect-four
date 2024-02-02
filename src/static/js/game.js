import { Subject } from "./subject.js"

export class Game {
	constructor(server, computerMoveDelay = 0) {
		this._board = make2DBoard(6, 7);
		this._server = server;
		this._isComputerThinking = false;
		this._computerMoveDelay = computerMoveDelay;
		this._subject = new Subject();
	}

	getCellState(row, col) {
		return this._board[row][col];
	}

	dropCoin(colIndex, whoseMove) {
		whoseMove = (whoseMove === undefined) ? "player" : whoseMove;
		for (let i = 0; i < 6; i++) {
			if (this._board[i][colIndex] === "empty") {
				this._board[i][colIndex] = whoseMove;
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

		for (let row = 0; row < this._board.length; row++) {
			for (let col = 0; col < this._board[row].length; col++) {
				for (const direction of directions) {
					if (this._checkWinningLine(row, col, direction.x, direction.y)) {
						return this._board[row][col];
					}
				}
			}
		}

		return "";
	}

	addListener(event, listener) {
		this._subject.addListener(event, listener);
	}

	async notify(event, data) {
		return this._subject.notify(event, data);
	}

	async makeComputerMove() {
		this._isComputerThinking = true;
		this.notify("computerStartThinking", {});

		const computerMove = await this._server.getComputerMove(this._encodeBoard());
		await new Promise(resolve => setTimeout(resolve, this._computerMoveDelay));
		this.dropCoin(computerMove, "computer");

		this._isComputerThinking = false;
		this.notify("computerStopThinking", {});
	}

	isComputerThinking() {
		return this._isComputerThinking;
	}

	_checkWinningLine(row, col, dx, dy) {
		const initialCell = this._board[row][col];
		if (initialCell === "empty") return false;

		for (let i = 1; i < 4; i++) {
			const newRow = row + i * dx;
			const newCol = col + i * dy;
			if (newRow < 0 || newRow >= this._board.length || newCol < 0 || newCol >= this._board[row].length) {
				return false;
			}
			if (this._board[newRow][newCol] !== initialCell) {
				return false;
			}
		}
		return true;
	}

	_encodeBoard() {
		let result = "";
		for (let row of this._board) {
			for (let state of row) {
				let char;
				switch (state) {
					case "player":
						char = "P";
						break;
					case "computer":
						char = "C";
						break;
					case "empty":
						char = "E";
						break;
					default:
						console.error("Got unknown cell state")
				}
				result = result.concat(char);
			}
			result = result.concat("|");
		}
		result = result.slice(0, -1);
		return result;
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
