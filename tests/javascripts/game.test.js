import { Game, make2DBoard } from "game.js";
import { test, expect, jest } from "@jest/globals";

test("create a Game object without problem", () => {
	const game = new Game();

	expect(game).toBeDefined();
});

test("all cell should be emptied on start", () => {
	const game = new Game(100);

	for (var i = 0; i < 6; i++) {
		for (var j = 0; j < 6; j++) {
			expect(game.getCellState(j, i)).toBe("empty");
		}
	}
});

test("drop multiple coins should stack up properly", () => {
	const game = new Game(100);

	game.dropCoin(0);
	game.dropCoin(0);
	game.dropCoin(1);

	let expectedBoard = make2DBoard(6, 7);
	expectedBoard[0][0] = "player";
	expectedBoard[1][0] = "player";
	expectedBoard[0][1] = "player";
	expect(game.board).toEqual(expectedBoard);
});