import { p5View } from "view.js";
import { Server } from "server.js"
import { Controller } from "controller.js";
import { Game } from "game.js";
import { jest, expect, describe } from "@jest/globals";

describe("when there are mocks", () => {

	let game, view, mockServer, controller;

	beforeEach(() => {
		game = new Game();
		view = new p5View(game, {}, 100);
		mockServer = { getComputerMove: jest.fn().mockResolvedValue(1) };
		controller = new Controller(game, view, mockServer);
	})

	test("controller should handle mouse click", () => {
		const spy = jest.spyOn(controller, "handleMouseClick");

		view.notify("mouseClick", { x: 10, y: 10 });

		expect(spy).toHaveBeenCalledWith(10, 10);
	});

	test("controller should use the computer move from the server to response player", async () => {
		await view.notify("mouseClick", { x: 10, y: 100 });

		expect(mockServer.getComputerMove).toHaveBeenCalledWith("PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE")
		expect(game.getCellState(0, 1)).toEqual("computer");
	});

	test("computer should not response to non-player move", () => {
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
		view.notify("mouseClick", { x: 10, y: 100 });

		expect(mockServer.getComputerMove).toHaveBeenCalledWith("PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE")
	});
})

describe("when there are no mocks (except p5)", () => {

	let game, view, server, controller;

	beforeEach(() => {
		game = new Game();
		view = new p5View(game, {}, 100);
		server = new Server("http://localhost:8000");
		controller = new Controller(game, view, server);
	})

	test("computer should response to player move", async () => {
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
		await view.notify("mouseClick", { x: 10, y: 100 });
		await view.notify("mouseClick", { x: 10, y: 100 });
		await view.notify("mouseClick", { x: 10, y: 100 });
		await view.notify("mouseClick", { x: 10, y: 100 });

		expect(game.getWinner()).toEqual("player");
	})

	test("the computer can win the game", async () => {
		await view.notify("mouseClick", { x: 10, y: 100 });
		await view.notify("mouseClick", { x: 10, y: 100 });
		await view.notify("mouseClick", { x: 10, y: 100 });
		await view.notify("mouseClick", { x: 310, y: 100 });

		expect(game.getWinner()).toEqual("computer");
	})

	test("should not response to player's click when the computer is thinking", async () => {
		const firstPromise = view.notify("mouseClick", { x: 10, y: 100 });
		const secondPromise = view.notify("mouseClick", { x: 210, y: 100 });
		await secondPromise;
		await firstPromise;

		expect(game.getCellState(0, 0)).toEqual("player");
		expect(game.getCellState(0, 1)).toEqual("computer");
		expect(game.getCellState(0, 2)).not.toEqual("player");
		expect(game.getCellState(1, 1)).not.toEqual("computer");
	})
})