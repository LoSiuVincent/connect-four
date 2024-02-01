export class Controller {
	constructor(game, view) {
		this.game = game;
		this.view = view;

		this.view.addListener("mouseClick", this);
	}

	async update(data) {
		await this.handleMouseClick(data.x, data.y);
	}

	async handleMouseClick(x, y) {
		if (this.view.isInsideCanvas(x, y) && !this.game.isComputerThinking()) {
			const colIndex = Math.floor(x / this.view.getCellLength());
			this.game.dropCoin(colIndex);
			await this.game.makeComputerMove();
		}
	}
}
