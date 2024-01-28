export class Game {
	constructor(cellLength) {
        this.cellLength = cellLength;
    }

    getCellLength() {
        return this.cellLength;
    }

    getCanvasWidth() {
        return this.cellLength * 7;
    }

    getCanvasHeight() {
        return this.cellLength * 8;
    }
}