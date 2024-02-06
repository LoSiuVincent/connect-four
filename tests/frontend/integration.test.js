/**
 * @jest-environment jsdom
 */

import { p5View } from "view.js";
import { Server } from "server.js"
import { Controller } from "controller.js";
import { Game } from "game.js";
import { jest, expect, describe } from "@jest/globals";

async function notifyClickColumn(view, colIndex) {
	return view.notify("mouseClick", { x: 10 + colIndex * 100, y: 10 });
}

describe("when there is server mock", () => {

	let game, view, mockServer, controller;

	beforeEach(() => {
		mockServer = { getComputerMove: jest.fn().mockResolvedValue(1) };
		game = new Game(mockServer);
		view = new p5View(game, {}, 100);
		controller = new Controller(game, view);
	})

	test("controller should handle mouse click", async () => {
		const spy = jest.spyOn(controller, "handleMouseClick");

		await notifyClickColumn(view, 0);

		expect(spy).toHaveBeenCalledWith(10, 10);
	});

	test("controller should not handle mouse click when the column is full", async () => {
		const spy = jest.spyOn(controller, "handleMouseClick");
		for (let i = 0; i < 3; i++) {
			game.dropCoin(0);
			game.dropCoin(0, "computer");
		}

		await notifyClickColumn(view, 0);

		expect(spy).not.toHaveBeenCalled();
	})

	test("should use the computer move from the server to response player", async () => {
		await notifyClickColumn(view, 0);

		expect(mockServer.getComputerMove).toHaveBeenCalledWith("PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE")
		expect(game.getCellState(0, 1)).toEqual("computer");
	});

	test("computer should not response to non-player move", () => {
		notifyClickColumn(view, -1);

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
		notifyClickColumn(view, 0);

		expect(mockServer.getComputerMove).toHaveBeenCalledWith("PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE")
	});
})

describe("when there are no mocks (except p5)", () => {

	let game, view, server, controller;

	beforeEach(() => {
		server = new Server("http://localhost:8000");
		game = new Game(server);
		view = new p5View(game, {}, 100);
		controller = new Controller(game, view);
	})

	test("computer should response to player move", async () => {
		await notifyClickColumn(view, 0);

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
		await notifyClickColumn(view, 0);
		await notifyClickColumn(view, 0);
		await notifyClickColumn(view, 0);
		await notifyClickColumn(view, 0);

		expect(game.getWinner()).toEqual("player");
	})

	test("the computer can win the game", async () => {
		await notifyClickColumn(view, 0);
		await notifyClickColumn(view, 0);
		await notifyClickColumn(view, 0);
		await notifyClickColumn(view, 3);

		expect(game.getWinner()).toEqual("computer");
	})

	test("should not response to player's click when the computer is thinking", async () => {
		const firstPromise = notifyClickColumn(view, 0);
		const secondPromise = notifyClickColumn(view, 2);
		await secondPromise;
		await firstPromise;

		expect(game.getCellState(0, 0)).toEqual("player");
		expect(game.getCellState(0, 1)).toEqual("computer");
		expect(game.getCellState(0, 2)).not.toEqual("player");
		expect(game.getCellState(1, 1)).not.toEqual("computer");
	})

	test("View should change state text when the computer start and stop thinking", async () => {
		const spy = jest.spyOn(view, "changeStateText");

		const playerClick = notifyClickColumn(view, 0, false);
		expect(spy).toHaveBeenCalledWith("Thinking ...");

		await playerClick;
		expect(spy).toHaveBeenCalledWith("Your turn");
	})

	test("Game can announce player wins and stop", async () => {
		const spy = jest.spyOn(view, "changeStateText");

		await notifyClickColumn(view, 0);
		await notifyClickColumn(view, 0);
		await notifyClickColumn(view, 0);
		await notifyClickColumn(view, 0);

		expect(spy).toHaveBeenLastCalledWith("You win!")

		const totalComputerMove = () => {
			let count = 0
			for (let i = 0; i < 6; i++) {
				for (let j = 0; j < 7; j++) {
					if (game.getCellState(i, j) === "computer") {
						count++;
					}
				}
			}
			return count;
		};
		expect(totalComputerMove()).toBe(3);
	})

	test("Game can announce player loses and stop", async () => {
		const spy = jest.spyOn(view, "changeStateText");

		await notifyClickColumn(view, 0);
		await notifyClickColumn(view, 0);
		await notifyClickColumn(view, 0);
		await notifyClickColumn(view, 3);

		expect(spy).toHaveBeenLastCalledWith("You lose, try again!")
	})
})