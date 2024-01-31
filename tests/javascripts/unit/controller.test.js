import { test, expect, jest } from "@jest/globals";
import { Controller } from "controller.js";
import { make2DBoard } from "game.js";

test("controller should call the correct dropCoin when receieve the mouse click event", () => {
	const mockGame = {
		dropCoin: jest.fn(),
	};
	const mockView = {
		getCellLength: () => 100,
		addListener: () => {},
		isInsideCanvas: () => true
	};
	const controller = new Controller(mockGame, mockView);

	for (var i = 0; i < 7; i++) {
		controller.handleMouseClick(50 + 100 * i, 10);
		expect(mockGame.dropCoin).toHaveBeenCalledWith(i);
	}
});

test("controller should add itself to listen on View", () => {
	const mockGame = {};
	const mockView = {addListener: jest.fn()};
	const controller = new Controller(mockGame, mockView);

	expect(mockView.addListener).toHaveBeenCalledWith("mouseClick", controller);
})

test("controller encode board to correct string", () => {
	const mockGame = {};
	const mockView = {addListener: jest.fn()};
	const controller = new Controller(mockGame, mockView);
	const board = make2DBoard(6, 7);
	board[0][0] = "player";
	board[1][0] = "computer";

	expect(controller._encodeBoard(board)).toEqual("PEEEEEE|CEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE");
})