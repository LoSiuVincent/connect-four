export class Controller {
	constructor(game, view) {
		this._game = game;
		this._view = view;

		this._view.addListener("mouseClick", this);
	}

	async update(data) {
		await this.handleMouseClick(data.x, data.y);
	}

	async handleMouseClick(x, y) {
		if (this._view.isInsideCanvas(x, y) && !this._game.isComputerThinking()) {
			const colIndex = Math.floor(x / this._view.getCellLength());
			this._game.dropCoin(colIndex);
			await this._game.makeComputerMove();
		}
	}
}
