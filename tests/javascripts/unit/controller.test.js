import { Controller } from "controller.js";
import { test, expect, jest } from "@jest/globals";

test("controller should call the correct dropCoin when receieve the mouse click event", () => {
	const mockGame = {
		dropCoin: jest.fn(),
	};
	const mockView = {
		getCellLength: () => {
			return 100;
		},
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