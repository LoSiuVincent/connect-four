export class Game {
	constructor(cellLength) {
		this.cellLength = cellLength;
		this.board = make2DBoard(6, 7);
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
		for (var i = 0; i < 6; i++) {
			if (this.board[i][colIndex] === "empty") {
				this.board[i][colIndex] = "player";
			}
		}
	}

	run() {
		new p5((p5) => {
			p5.setup = () => {
				p5.createCanvas(this.getCanvasWidth(), this.getCanvasHeight());
			};

			p5.draw = () => {
				p5.fill(0);
			};
		});
	}
}

function make2DBoard(rows, cols) {
	var board = [];
	for (var i = 0; i < rows; i++) {
		board[i] = [];
		for (var j = 0; j < cols; j++) {
			board[i][j] = "empty";
		}
	}
    return board;
}
