import { Subject } from "./subject.js";

export class p5View {
	constructor(game, p5, cellLength) {
		this._game = game;
		this._p5 = p5;
		this._cellLength = cellLength === undefined ? 100 : cellLength;
		this._subject = new Subject();

		this._p5.mouseClicked = () => {
			this.notify("mouseClick", { x: this._p5.mouseX, y: this._p5.mouseY });
		};
		this._game.addListener("computerStartThinking", this);
		this._game.addListener("computerStopThinking", this);
	}

	getCellLength() {
		return this._cellLength;
	}

	getCanvasWidth() {
		return this._cellLength * 7;
	}

	getCanvasHeight() {
		return this._cellLength * 8;
	}

	isInsideCanvas(x, y) {
		return (0 <= x && x <= this.getCanvasWidth()) && (0 <= y && y <= this.getCanvasHeight());
	}

	changeStateText(text) {

	}

	async update(event, data) {
		if (event === "computerStartThinking") {
			this.changeStateText("Thinking ...");
		} else if (event === "computerStopThinking") {
			this.changeStateText("Your turn");
		}
	}

	draw() {
		this._drawBoard();
	}

	addListener(event, listener) {
		this._subject.addListener(event, listener);
	}

	async notify(event, data) {
		return this._subject.notify(event, data);
	}

	_getCell(row, col) {
		const cornerX = col * this._cellLength;
		const cornerY = (7 - row) * this._cellLength;
		const centerX = cornerX + this._cellLength / 2;
		const centerY = cornerY + this._cellLength / 2;
		return { cornerX, cornerY, centerX, centerY, };
	}

	_drawCell(row, col) {
		const cell = this._getCell(row, col);

		this._p5.fill(255, 255, 255);
		this._p5.stroke(0, 0, 0);
		this._p5.strokeWeight(4);
		this._p5.square(cell.cornerX, cell.cornerY, this._cellLength);
	}

	_drawCoin(row, col) {
		const cell = this._getCell(row, col);
		const diameter = this._cellLength * 0.75;

		const cellState = game.getCellState(row, col);
		if (cellState === "player") {
			this._p5.fill(255, 0, 0);
		} else if (cellState === "computer") {
			this._p5.fill(255, 204, 0);
		}
		this._p5.noStroke();
		this._p5.circle(cell.centerX, cell.centerY, diameter);
	}

	_drawBoard() {
		for (let i = 0; i < 6; i++) {
			for (let j = 0; j < 7; j++) {
				this._drawCell(i, j);
				if (this._game.getCellState(i, j) === "player" || this._game.getCellState(i, j) === "computer") {
					this._drawCoin(i, j);
				}
			}
		}
	}
}
