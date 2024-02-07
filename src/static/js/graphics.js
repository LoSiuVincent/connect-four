const CELL_COUNT_X = 7;
const CELL_COUNT_Y = 6;
const BOARD_COLOR = '#007FFF'; // Deep sky blue
const PLAYER_COLOR = '#FF0000'; // Red
const COMPUTER_COLOR = '#FFCC00'; // Yellow
const DEFAULT_CELL_LENGTH = 100;
const COIN_SPAWN_Y = DEFAULT_CELL_LENGTH / 2;

export class Graphics {
	constructor(p5, cellLength, game) {
		this._p5 = p5;
		this._cellLength = cellLength === undefined ? DEFAULT_CELL_LENGTH : cellLength;
		this._game = game;
		this._coins = [];
	}

	setup() {
		this._p5.setAttributes('antialias', true);
		this._canvas = this._p5.createCanvas(this.getCanvasWidth(), this.getCanvasHeight());
		this._pg = this._p5.createGraphics(this.getCanvasWidth(), this._cellLength * 6);
	}

	update() {

	}

	draw() {
		this._drawAllCoins();
		this._drawBoard();
		this._p5.image(this._pg, 0, 2 * this._cellLength);
	}

	getCellLength() {
		return this._cellLength;
	}

	getCanvasWidth() {
		return this._cellLength * CELL_COUNT_X;
	}

	getCanvasHeight() {
		return this._cellLength * (CELL_COUNT_Y + 2);
	}

	addCoin(row, col, whose) {
		const newCoin = new Coin(row, col, whose, this._cellLength, this._p5);
		this._coins.push(newCoin);
	}

	_drawAllCoins() {
		for (const coin of this._coins) {
			coin.draw();
		}
	}

	_drawBoard() {
		const diameter = this._cellLength * 0.7;

		this._pg.background(BOARD_COLOR);
		for (let row = 0; row < CELL_COUNT_Y; row++) {
			for (let col = 0; col < CELL_COUNT_X; col++) {
				const centerX = col * this._cellLength + this._cellLength / 2;
				const centerY = (CELL_COUNT_Y - 1 - row) * this._cellLength + this._cellLength / 2;

				this._pg.erase(255, 255);
				this._pg.circle(centerX, centerY, diameter);
				this._pg.noErase();
			}
		}
	}
}

class Coin {
	constructor(row, col, whose, cellLength, p5) {
		this._row = row;
		this._col = col;
		this._whose = whose;
		this._cellLength = cellLength
		this._diameter = cellLength * 0.75;
		this._p5 = p5;
		this._coinCenterX = this._col * this._cellLength + this._cellLength / 2;
		this._coinCenterY = (CELL_COUNT_Y + 1 - this._row) * this._cellLength + this._cellLength / 2;
	}

	draw() {
		if (this._whose === "player") {
			this._p5.fill(PLAYER_COLOR);
		} else if (this._whose === "computer") {
			this._p5.fill(COMPUTER_COLOR);
		}
		this._p5.noStroke();

		this._p5.circle(this._coinCenterX, this._coinCenterY, this._diameter);
	}
}