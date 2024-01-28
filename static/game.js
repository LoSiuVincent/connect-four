import { p5View } from "./view.js";

export class Game {
	constructor(cellLength, view) {
		this.cellLength = cellLength;
		this.board = make2DBoard(6, 7);
		this.view = (view === undefined) ? new p5View() : view;

		this.view.drawBoard(this.board);
	}

	getCellLength() {
		return this.cellLength;
	}

	getCanvasWidth() {
		return this.cellLength * 7;
	}

	getCanvasHeight() {
		return this.cellLength * 8;
	}

	getCellState(col, row) {
		return this.board[row][col];
	}

	dropCoin(colIndex) {
		for (let i = 0; i < 6; i++) {
			if (this.board[i][colIndex] === "empty") {
				this.board[i][colIndex] = "player";
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
