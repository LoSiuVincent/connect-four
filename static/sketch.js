import { Game } from "./game.js";
import { p5View } from "./view.js";

new p5((p5) => {
	p5.setup = () => {
		const CELL_SIZE = 100;
		const game = new Game();
		const view = new p5View(game, p5, CELL_SIZE);
		p5.createCanvas(view.getCanvasWidth(), view.getCanvasHeight());

		window.game = game;
		window.view = view;
	};

	p5.draw = () => {
		window.view.draw();
	};
});
