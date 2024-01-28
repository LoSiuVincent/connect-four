import { Game } from "../static/game.js";

test("create a Game object without problem", () => {
	const game = new Game();
});

test("get cell length from the Game object", () => {
	const game = new Game(100);

	expect(game.getCellLength()).toBe(100);
});

test("Game has the correct canvas width", () => {
	const game = new Game(100);
	const biggerGame = new Game(150);

	expect(game.getCanvasWidth()).toBe(700);
	expect(biggerGame.getCanvasWidth()).toBe(1050);
});

test("Game has the correct canvas height", () => {
	const game = new Game(100);
	const biggerGame = new Game(150);

	expect(game.getCanvasHeight()).toBe(800);
	expect(biggerGame.getCanvasHeight()).toBe(1200);
});
