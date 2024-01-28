import { Game } from "./game.js";

window.game = new Game();

new p5((p5) => {
	p5.setup = () => {
		p5.createCanvas(1024, 800);
	};

	p5.draw = () => {
		p5.fill(0);
	};
});
