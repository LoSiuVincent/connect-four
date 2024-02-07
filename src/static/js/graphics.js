const CELL_COUNT_X = 7;
const CELL_COUNT_Y = 6;
const BOARD_COLOR = '#007FFF'; // Deep sky blue
const PLAYER_COLOR = '#FF0000'; // Red
const COMPUTER_COLOR = '#FFCC00'; // Yellow
const BACKGROUND_COLOR = '#FFFFFF'; // White
const DEFAULT_CELL_LENGTH = 100;
const COIN_SPAWN_Y = DEFAULT_CELL_LENGTH / 2;
const COIN_DROP_DY = 3;
const COIN_DROP_ACCELERATION = 1;

export class Graphics {
	constructor(p5, cellLength, game) {
		this._p5 = p5;
		this._cellLength = cellLength === undefined ? DEFAULT_CELL_LENGTH : cellLength;
		this._game = game;
		this._coinManager = new CoinManager(this._cellLength, this._p5);
	}

	setup() {
		this._p5.setAttributes('antialias', true);
		this._canvas = this._p5.createCanvas(this.getCanvasWidth(), this.getCanvasHeight());
		this._pg = this._p5.createGraphics(this.getCanvasWidth(), this._cellLength * 6);
	}

	update() {
		this._coinManager.update();
	}

	draw() {
		this._p5.background(BACKGROUND_COLOR);
		this._coinManager.draw();
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
		this._coinManager.addCoin(row, col, whose);
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

class CoinManager {
	constructor(cellLength, p5) {
		this._cellLength = cellLength;
		this._p5 = p5;
		this._coins = [];
	}

	addCoin(row, col, whose) {
		const newCoin = new Coin(row, col, whose, this._cellLength, this._p5);
		this._coins.push(newCoin);
	}

	update() {
		for (const coin of this._coins) {
			coin.update();
		}
	}

	draw() {
		for (const coin of this._coins) {
			coin.draw();
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
		this._x = this._col * this._cellLength + this._cellLength / 2;
		this._y = COIN_SPAWN_Y;
		this._y_stop = (CELL_COUNT_Y + 1 - this._row) * this._cellLength + this._cellLength / 2;
		this._isDropping = true;
		this._dy = COIN_DROP_DY
	}

	update() {
		if (this._isDropping) {
			this._y += this._dy;
			this._dy += COIN_DROP_ACCELERATION;
			if (this._y > this._y_stop) {
				this._y = this._y_stop;
				this._isDropping = false;
			}
		}
	}

	draw() {
		if (this._whose === "player") {
			this._p5.fill(PLAYER_COLOR);
		} else if (this._whose === "computer") {
			this._p5.fill(COMPUTER_COLOR);
		}
		this._p5.noStroke();

		this._p5.circle(this._x, this._y, this._diameter);
	}
}