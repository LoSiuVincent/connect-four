export class Game {
	constructor(boardX, boardY, cellWidth) {
        this.boardX = boardX;
        this.boardY = boardY;
        this.cellWidth = cellWidth;
    }

    getBoardX() {
        return this.boardX;
    }

    getBoardY() {
        return this.boardY;
    }

    getCellWidth() {
        return this.cellWidth;
    }
}