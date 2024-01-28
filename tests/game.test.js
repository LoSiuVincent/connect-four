import { Game } from "../static/game.js";

test("create a Game object without problem", () => {
	const game = new Game();

	expect(game).toBeDefined();
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

test("all cell should be emptied on start", () => {
	const game = new Game(100);

	for (var i = 0; i < 6; i++) {
		for (var j = 0; j < 6; j++) {
			expect(game.getCellState(j, i)).toBe("empty");
		}
	}
})

test("drop a coin in the first column should change the bottom cell state to player", () => {
	const game = new Game(100);

	game.dropCoin(0);

	expect(game.getCellState(0, 0)).toBe("player");
})

test("drop multiple coin in the same column should stack up the coin", () => {
	const game = new Game(100);

	game.dropCoin(0);
	game.dropCoin(0);
	game.dropCoin(0);

	expect(game.getCellState(0, 0)).toBe("player");
	expect(game.getCellState(0, 1)).toBe("player");
	expect(game.getCellState(0, 2)).toBe("player");
})