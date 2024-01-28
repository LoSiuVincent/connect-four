import { Game } from "../static/game.js";

test("create a Game object without problem", () => {
	const game = new Game();
});

test("get board x from the Game object", () => {
	const game = new Game(10);

	expect(game.getBoardX()).toBe(10);
})

test("get board y from the Game object", () => {
	const game = new Game(10, 20);

	expect(game.getBoardY()).toBe(20);
})

test("get cell width from the Game object", () => {
	const game = new Game(10, 20, 100);

	expect(game.getCellWidth()).toBe(100);
})