import { Game } from "./js/game.js";
import { p5View } from "./js/view.js";
import { Controller } from "./js/controller.js";
import { Server } from "./js/server.js";

new p5((p5) => {
	p5.setup = () => {
		const CELL_SIZE = 100;
		const game = new Game();
		const view = new p5View(game, p5, CELL_SIZE);
		const server = new Server();
		p5.createCanvas(view.getCanvasWidth(), view.getCanvasHeight());

		window.game = game;
		window.view = view;
		window.controller = new Controller(game, view, server, true);
	};

	p5.draw = () => {
		window.view.draw();
	};
});
