import { Game } from "../static/game.js";

test("create a Game object without problem", () => {
	const game = new Game();
});

test("get cell length from the Game object", () => {
	const game = new Game(100);

	expect(game.getCellLength()).toBe(100);
});
