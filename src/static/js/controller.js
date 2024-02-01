export class Controller {
	constructor(game, view, server, delayComputerMove = false) {
		this.game = game;
		this.view = view;
		this.server = server;
		this.delayComputerMove = delayComputerMove;
		this.isComputerThinking = false;

		this.view.addListener("mouseClick", this);
	}

	async update(data) {
		await this.handleMouseClick(data.x, data.y);
	}

	async handleMouseClick(x, y) {
		if (this.view.isInsideCanvas(x, y) && !this.game.isComputerThinking()) {
			const colIndex = Math.floor(x / this.view.getCellLength());
			this.game.dropCoin(colIndex);
			this.game.makeComputerMove();
		}
	}
}
