import { Game } from "./game.js";
import { p5View } from "./view.js";

const CELL_SIZE = 100;
const game = new Game(CELL_SIZE);
window.game = game;

new p5((p5) => {
	p5.setup = () => {
		p5.createCanvas(game.getCanvasWidth(), game.getCanvasHeight());
		window.view = new p5View(game, p5);
	};

	p5.draw = () => {
		window.view.draw();
	};
});
