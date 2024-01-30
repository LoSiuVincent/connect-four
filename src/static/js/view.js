export class p5View {
	constructor(game, p5, cellLength) {
		this.game = game;
		this.p5 = p5;
		this.cellLength = cellLength === undefined ? 100 : cellLength;
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

	draw() {
		this._drawBoard();
	}

	_drawCell(row, col) {
		const cellLength = this.cellLength;
		const cornerX = col * cellLength;
		const cornerY = 2 * cellLength + (5 - row) * cellLength;

		this.p5.fill(255, 255, 255);
		this.p5.stroke(0, 0, 0);
		this.p5.strokeWeight(4);
		this.p5.square(cornerX, cornerY, cellLength);
	}

	_drawCoin(row, col) {
		const diameter = this.cellLength * 0.75;
		const cornerX = col * this.cellLength;
		const cornerY = 2 * this.cellLength + (5 - row) * this.cellLength;
		const centerX = cornerX + this.cellLength / 2;
		const centerY = cornerY + this.cellLength / 2;

		this.p5.fill(255, 0, 0);
		this.p5.noStroke();
		this.p5.circle(centerX, centerY, diameter);
	}

	_drawBoard() {
		for (let i = 0; i < 6; i++) {
			for (let j = 0; j < 7; j++) {
				this._drawCell(i, j);
				if (this.game.getCellState(i, j) === "player") {
					this._drawCoin(i, j);
				}
			}
		}
	}
}
