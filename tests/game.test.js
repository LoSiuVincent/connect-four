import { Game } from "../static/game.js";

test("create a Game object without problem", () => {
	const game = new Game();
});

test("get board x from the Game object", () => {
	const game = new Game(10);

	expect(game.getBoardX()).toEqual(10);
})

test("get board y from the Game object", () => {
	const game = new Game(10, 20);

	expect(game.getBoardY()).toEqual(20);
})