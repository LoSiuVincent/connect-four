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
	};
	const controller = new Controller(mockGame, mockView);

	for (var i = 0; i < 7; i++) {
		controller.handleMouseClick(50 + 100 * i, 10);
		expect(mockGame.dropCoin).toHaveBeenCalledWith(i);
	}
});
