import { p5View } from "view.js";
import { Controller } from "controller.js";
import { jest, expect, describe } from "@jest/globals";
import { Game } from "../../src/static/js/game";

describe("integration", () => {
	test("controller should handle mouse click when view notify a mouse click event", () => {
		const mockGame = { dropCoin: jest.fn() };
		const view = new p5View(mockGame, {}, {});
		const controller = new Controller(mockGame, view, jest.fn());
		const spy = jest.spyOn(controller, "handleMouseClick");

		view.notify("mouseClick", { x: 10, y: 10 });

		expect(spy).toHaveBeenCalledWith(10, 10);
	});

	test("computer should response to player's move", () => {
		const game = new Game();
		const view = new p5View(game, {}, 100);
		const controller = new Controller(game, view, jest.fn());

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

	test("computer should not response to non-player move", () => {
		const game = new Game();
		const view = new p5View(game, {}, 100);
		const controller = new Controller(game, view, jest.fn());

		view.notify("mouseClick", { x: -10, y: 100 });

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
		expect(hasComputerMove()).toBe(false);
	});	
	
	test("controller should send a fetch request for a computer move", () => {
		const game = new Game();
		const view = new p5View(game, {}, 100);
		const spyFetch = jest.fn();
		const controller = new Controller(game, view, spyFetch);

		view.notify("mouseClick", { x: 10, y: 100 });

		expect(spyFetch).toHaveBeenCalledWith("/predict", {
			method: "POST",
			body: "PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE",
		})
	});
});
