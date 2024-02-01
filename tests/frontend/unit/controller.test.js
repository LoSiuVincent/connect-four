import { test, expect, jest } from "@jest/globals";
import { Controller } from "controller.js";

function createMocks() {
	const mockGame = {
		dropCoin: jest.fn(),
		makeComputerMove: jest.fn(),
		isComputerThinking: jest.fn().mockReturnValue(false),
		board: [[]],
	};
	const mockView = {
		getCellLength: jest.fn().mockReturnValue(100),
		addListener: jest.fn(),
		isInsideCanvas: jest.fn().mockReturnValue(true),
		notify: jest.fn(),
	};

	return { mockGame, mockView };
}

test("controller should call the correct dropCoin when receive the mouse click event", async () => {
	const { mockGame, mockView } = createMocks();
	const controller = new Controller(mockGame, mockView);

	for (let i = 0; i < 7; i++) {
		await controller.handleMouseClick(50 + 100 * i, 10);
		expect(mockGame.dropCoin).toHaveBeenCalledWith(i);
	}
});

test("controller should ask the for a computer move when the player make a move", async () => {
	const { mockGame, mockView } = createMocks();
	const controller = new Controller(mockGame, mockView);

	await controller.handleMouseClick(10, 10);
	expect(mockGame.makeComputerMove).toHaveBeenCalled();
});

test("controller should not ask for a computer move when the player does not make a move", async () => {
	const { mockGame, mockView } = createMocks();
	mockView.isInsideCanvas = jest.fn().mockReturnValue(false);
	const controller = new Controller(mockGame, mockView);

	await controller.handleMouseClick(-10, 10);
	expect(mockGame.makeComputerMove).not.toHaveBeenCalled();
});

test("controller should not ask for a computer move when it is thinking", async () => {
	const { mockGame, mockView } = createMocks();
	mockGame.isComputerThinking = jest.fn().mockReturnValue(true);
	const controller = new Controller(mockGame, mockView);

	await controller.handleMouseClick(10, 10);
	expect(mockGame.makeComputerMove).not.toHaveBeenCalled();
});

test("controller should add itself to listen on View", () => {
	const { mockGame, mockView } = createMocks();
	const controller = new Controller(mockGame, mockView);

	expect(mockView.addListener).toHaveBeenCalledWith("mouseClick", controller);
});
