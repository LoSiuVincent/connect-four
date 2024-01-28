import { Game } from "./game.js";

const CELL_SIZE = 100;
const game = new Game(CELL_SIZE);
window.game = game;

new p5((p5) => {
	p5.setup = () => {
		p5.createCanvas(game.getCanvasWidth(), game.getCanvasHeight());
	};

	p5.draw = () => {
	};
});
