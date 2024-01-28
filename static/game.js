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

	run() {
		new p5((p5) => {
			p5.setup = () => {
				p5.createCanvas(1024, 800);
			};

			p5.draw = () => {
				p5.fill(0);
			};
		});
	}
}
