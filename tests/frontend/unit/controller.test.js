import { test, expect, jest } from "@jest/globals";
import { Controller } from "controller.js";
import { make2DBoard } from "game.js";

function createMocks() {
	const mockGame = {
		dropCoin: jest.fn(),
		board: [[]],
	};
	const mockView = {
		getCellLength: jest.fn().mockReturnValue(100),
		addListener: jest.fn(),
		isInsideCanvas: jest.fn().mockReturnValue(true),
		notify: jest.fn(),
	};
	const mockServer = {
		getComputerMove: jest.fn().mockResolvedValue(0),
	};

	return { mockGame, mockView, mockServer };
}

test("controller should call the correct dropCoin when receive the mouse click event", async () => {
	const { mockGame, mockView, mockServer } = createMocks();
	const controller = new Controller(mockGame, mockView, mockServer);

	for (let i = 0; i < 7; i++) {
		await controller.handleMouseClick(50 + 100 * i, 10);
		expect(mockGame.dropCoin).toHaveBeenCalledWith(i);
	}
});

test("controller should add itself to listen on View", () => {
	const { mockGame, mockView } = createMocks();
	const controller = new Controller(mockGame, mockView);

	expect(mockView.addListener).toHaveBeenCalledWith("mouseClick", controller);
});

test("controller encode board to correct string", () => {
	const { mockGame, mockView } = createMocks();
	const controller = new Controller(mockGame, mockView);
	const board = make2DBoard(6, 7);
	board[0][0] = "player";
	board[1][0] = "computer";

	expect(controller._encodeBoard(board)).toEqual("PEEEEEE|CEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE");
});

test("controller should not make computer move when it is thinking", async () => {
	const { mockGame, mockView, mockServer } = createMocks();
	const controller = new Controller(mockGame, mockView, mockServer);
	const spy = jest.spyOn(controller, "makeComputerMove");

	const firstPromise = controller.handleMouseClick(10, 10);
	const secondPromise = controller.handleMouseClick(10, 10);
	await secondPromise;
	await firstPromise;

	expect(spy).toHaveBeenCalledTimes(1);
});