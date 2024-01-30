export class Controller {
    constructor(game, view) {
        this.game = game;
        this.view = view;

        this.view.addListener("mouseClick", this);
    }

    update(data) {
        this.handleMouseClick(data.x, data.y);
    }

    handleMouseClick(x, y) {
        const colIndex = Math.floor(x / this.view.getCellLength());
        this.game.dropCoin(colIndex);
    }
}