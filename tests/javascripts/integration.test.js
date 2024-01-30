import { p5View } from "view.js";
import { Controller } from "controller.js";
import { jest, expect, describe } from "@jest/globals";

describe("integration", () => {
	test("controller should handle mouse click when view notify a mouse click event", () => {
		const mockGame = {dropCoin: jest.fn()};
		const view = new p5View(mockGame, {}, {});
		const controller = new Controller(mockGame, view);
		const spy = jest.spyOn(controller, "handleMouseClick");

		view.notify("mouseClick", { x: 10, y: 10 });

		expect(spy).toHaveBeenCalledWith(10, 10);
	});
});
