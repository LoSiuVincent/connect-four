export class Game {
	constructor(cellLength) {
		this.cellLength = cellLength;
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
        return "empty";
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
