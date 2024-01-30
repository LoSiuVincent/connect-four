import { p5View } from "view.js";
import { Controller } from "controller.js";
import { jest, expect, describe } from "@jest/globals";
import { Game } from "../../src/static/js/game";

describe("integration", () => {
	test("controller should handle mouse click when view notify a mouse click event", () => {
		const mockGame = { dropCoin: jest.fn() };
		const view = new p5View(mockGame, {}, {});
		const controller = new Controller(mockGame, view);
		const spy = jest.spyOn(controller, "handleMouseClick");

		view.notify("mouseClick", { x: 10, y: 10 });

		expect(spy).toHaveBeenCalledWith(10, 10);
	});

	test("computer can response to player's move", () => {
		const game = new Game();
		const view = new p5View(game, {}, 100);
		const controller = new Controller(game, view);

		view.notify("mouseClick", { x: 10, y: 100 });

		const hasComputerMove = () => {
			for (let i = 0; i < 6; i++) {
				for (let j = 0; j < 7; j++) {
					if (game.getCellState(i, j) === "computer") {
						return true;
					}
				}
			}
			return false;
		};
		expect(hasComputerMove()).toBe(true);
	});
});
