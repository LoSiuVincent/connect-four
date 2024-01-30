export class Controller {
    constructor(game, view) {
        this.game = game;
        this.view = view;

        this.view.addListener("mouseClick", this.handleMouseClick);
    }

    handleMouseClick(x, y) {
        const colIndex = Math.floor(x / this.view.getCellLength());
        this.game.dropCoin(colIndex);
    }
}