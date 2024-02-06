import { Game } from "./js/game.js";
import { p5View } from "./js/view.js";
import { Controller } from "./js/controller.js";
import { Server } from "./js/server.js";

new p5((p5) => {
	p5.setup = () => {
		const CELL_SIZE = 100;
		const server = new Server("", TEST);
		const game = new Game(server, TEST ? 800 : 2000);
		const view = new p5View(game, p5, CELL_SIZE);
		
		window.game = game;
		window.view = view;
		window.controller = new Controller(game, view);

		view.setup();
	};

	p5.draw = () => {
		window.view.draw();
	};
}, document.getElementById('game-canvas'));
