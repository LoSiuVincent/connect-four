import { Game } from "./js/game.js";
import { p5View } from "./js/view.js";
import { Controller } from "./js/controller.js";
import { Server } from "./js/server.js";

new p5((p5) => {
	p5.setup = () => {
		const CELL_SIZE = 100;
		const server = new Server("", false);
		const game = new Game(server, 2000);
		const view = new p5View(game, p5, CELL_SIZE);
		p5.createCanvas(view.getCanvasWidth(), view.getCanvasHeight());

		window.game = game;
		window.view = view;
		window.controller = new Controller(game, view);
	};

	p5.draw = () => {
		window.view.draw();
	};
});
