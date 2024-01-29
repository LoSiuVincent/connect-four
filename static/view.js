export class p5View {
	constructor(game, p5) {
		this.game = game;
		this.p5 = p5;
	}

	draw() {
		this._drawBoard();
	}

	_drawCell(row, col) {
		const cellLength = this.game.getCellLength();
		const cornerX = col * cellLength;
		const cornerY = 2 * cellLength + row * cellLength;

		this.p5.stroke(0, 0, 0);
		this.p5.strokeWeight(4);
		this.p5.square(cornerX, cornerY, cellLength);
	}

	_drawBoard() {
		for (let i = 0; i < 6; i++) {
			for (let j = 0; j < 7; j++) {
				this._drawCell(i, j);
			}
		}
	}
}
