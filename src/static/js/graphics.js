const CELL_COUNT_X = 7;
const CELL_COUNT_Y = 6;
const BOARD_COLOR = '#007FFF'; // Deep sky blue
const PLAYER_COLOR = '#FF0000'; // Red
const COMPUTER_COLOR = '#FFCC00'; // Yellow
const DEFAULT_CELL_LENGTH = 100;
const HOLE_STROKE_WEIGHT = 2;
const HOLE_STROKE_COLOR = '#000000';

export class Graphics {
	constructor(p5, cellLength, game) {
		this._p5 = p5;
		this._cellLength = cellLength === undefined ? DEFAULT_CELL_LENGTH : cellLength;
		this._game = game;
	}

	setup() {
		this._p5.setAttributes('antialias', true);
		this._canvas = this._p5.createCanvas(this.getCanvasWidth(), this.getCanvasHeight());
		this._pg = this._p5.createGraphics(this.getCanvasWidth(), this._cellLength * 6);
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

	_getCell(row, col) {
		const cornerX = col * this._cellLength;
		const cornerY = (CELL_COUNT_Y + 1 - row) * this._cellLength;
		const centerX = cornerX + this._cellLength / 2;
		const centerY = cornerY + this._cellLength / 2;
		return { cornerX, cornerY, centerX, centerY };
	}

	_drawAllCoins() {
		for (let i = 0; i < CELL_COUNT_Y; i++) {
			for (let j = 0; j < CELL_COUNT_X; j++) {
				if (this._game.getCellState(i, j) === "player" || this._game.getCellState(i, j) === "computer") {
					this._drawCoin(i, j);
				}
			}
		}
	}

	_drawCoin(row, col) {
		const cell = this._getCell(row, col);
		const diameter = this._cellLength * 0.75;

		const cellState = game.getCellState(row, col);
		if (cellState === "player") {
			this._p5.fill(PLAYER_COLOR);
		} else if (cellState === "computer") {
			this._p5.fill(COMPUTER_COLOR);
		}
		this._p5.noStroke();
		this._p5.circle(cell.centerX, cell.centerY, diameter);
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
