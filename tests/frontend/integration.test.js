import { p5View } from "view.js";
import { Server } from "server.js"
import { Controller } from "controller.js";
import { jest, expect, describe } from "@jest/globals";
import { Game } from "../../src/static/js/game";

describe("when player clicks on the first column", () => {
	describe("when there are mocks", () => {
		test("controller should handle mouse click", () => {
			const mockGame = { dropCoin: jest.fn() };
			const view = new p5View(mockGame, {}, {});
			const controller = new Controller(mockGame, view);
			const spy = jest.spyOn(controller, "handleMouseClick");

			view.notify("mouseClick", { x: 10, y: 10 });

			expect(spy).toHaveBeenCalledWith(10, 10);
		});

		test("controller should use the computer move from the server to response player", async () => {
			const game = new Game();
			const view = new p5View(game, {}, 100);
			const mockServer = { getComputerMove: jest.fn().mockResolvedValue(1) };
			const controller = new Controller(game, view, mockServer);

			await view.notify("mouseClick", { x: 10, y: 100 });

			expect(mockServer.getComputerMove).toHaveBeenCalledWith("PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE")
			expect(game.getCellState(0, 1)).toEqual("computer");
		});

		test("computer should not response to non-player move", () => {
			const game = new Game();
			const view = new p5View(game, {}, 100);
			const mockServer = { getComputerMove: () => 1 };
			const controller = new Controller(game, view, mockServer);

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

		test("controller should call getComputerMove from the server", () => {
			const game = new Game();
			const view = new p5View(game, {}, 100);
			const mockServer = { getComputerMove: jest.fn() };
			const controller = new Controller(game, view, mockServer);

			view.notify("mouseClick", { x: 10, y: 100 });

			expect(mockServer.getComputerMove).toHaveBeenCalledWith("PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE")
		});
	})

	describe("when there are no mocks (except p5)", () => {
		test("computer should response to player move", async () => {
			const game = new Game();
			const view = new p5View(game, {}, 100);
			const server = new Server("http://localhost:8000");
			const controller = new Controller(game, view, server);

			await view.notify("mouseClick", { x: 10, y: 100 });

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
		})

		test("the player can win the game", async () => {
			const game = new Game();
			const view = new p5View(game, {}, 100);
			const server = new Server("http://localhost:8000");
			const controller = new Controller(game, view, server);

			await view.notify("mouseClick", { x: 10, y: 100 });
			await view.notify("mouseClick", { x: 10, y: 100 });
			await view.notify("mouseClick", { x: 10, y: 100 });
			await view.notify("mouseClick", { x: 10, y: 100 });

			expect(game.getWinner()).toEqual("player");
		})

		test("the computer can win the game", async () => {
			const game = new Game();
			const view = new p5View(game, {}, 100);
			const server = new Server("http://localhost:8000");
			const controller = new Controller(game, view, server);

			await view.notify("mouseClick", { x: 10, y: 100 });
			await view.notify("mouseClick", { x: 10, y: 100 });
			await view.notify("mouseClick", { x: 10, y: 100 });
			await view.notify("mouseClick", { x: 310, y: 100 });

			expect(game.getWinner()).toEqual("computer");
		})
	})
})
