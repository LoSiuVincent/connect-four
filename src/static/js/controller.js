export class Controller {
	constructor(game, view) {
		this._game = game;
		this._view = view;

		this._view.addListener("mouseClick", this);
	}

	async update(event, data) {
		if (this._shouldResponseClick(data.x, data.y)) {
			await this.handleMouseClick(data.x, data.y);
		}
	}


	async handleMouseClick(x, y) {
		const colIndex = this._getColIndex(x);
		this._game.dropCoin(colIndex);
		if (this._game.getWinner() != "player") {
			await this._game.makeComputerMove();
		}
	}

	_shouldResponseClick(x, y) {
		return (!this._game.isEnded()
			&& !this._game.isComputerThinking()
			&& this._view.isInsideCanvas(x, y)
			&& !this._game.isColumnFull(this._getColIndex(x)));
	}

	_getColIndex(x) {
		return Math.floor(x / this._view.getCellLength());
	}
}
