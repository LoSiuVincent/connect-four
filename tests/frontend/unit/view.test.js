/**
 * @jest-environment jsdom
 */

import { p5View } from "view.js";
import { jest, expect, test } from "@jest/globals";

describe("p5View tests", () => {
	const createView = (cellLength = 100) => {
		const mockGame = { addListener: jest.fn() }
		const dummyObject = {};
		return new p5View(mockGame, dummyObject, cellLength);
	};

	test("View has the correct cell length", () => {
		const cellLength = 100;
		const view = createView(cellLength);
		expect(view.getCellLength()).toBe(cellLength);
	});

	describe("Canvas dimensions based on cell length", () => {
		test("View has the correct canvas width", () => {
			const view = createView(100);
			const biggerView = createView(150);
			expect(view.getCanvasWidth()).toBe(700);
			expect(biggerView.getCanvasWidth()).toBe(1050);
		});

		test("View has the correct canvas height", () => {
			const view = createView(100);
			const biggerView = createView(150);
			expect(view.getCanvasHeight()).toBe(800);
			expect(biggerView.getCanvasHeight()).toBe(1200);
		});
	});

	test("View should notify listeners when they subscribe to it", () => {
		const view = createView();
		const listenerOne = { update: jest.fn() };
		const listenerTwo = { update: jest.fn() };
		const listenerThree = { update: jest.fn() };
		view.addListener("mouseClick", listenerOne);
		view.addListener("mouseClick", listenerTwo);
		view.addListener("otherEvent", listenerThree);

		view.notify("mouseClick", { x: 10, y: 10 });

		expect(listenerOne.update).toHaveBeenCalledWith("mouseClick", { x: 10, y: 10 });
		expect(listenerTwo.update).toHaveBeenCalledWith("mouseClick", { x: 10, y: 10 });
		expect(listenerThree.update).not.toHaveBeenCalled();
	});

	test("isInsideCanvas should return correct value", () => {
		const view = createView();
		expect(view.isInsideCanvas(-10, 400)).toBe(false);
		expect(view.isInsideCanvas(200, 400)).toBe(true);
		expect(view.isInsideCanvas(800, 900)).toBe(false);
	});

	describe("change state text", () => {
		let view, spy;

		view = createView();
		spy = jest.spyOn(view, "changeStateText");

		test("should change state text when the computer starts thinking", () => {
			view.update("computerStartThinking", {});

			expect(spy).toHaveBeenCalledWith("Thinking ...")
		})

		test("should change state text when the computer stops thinking", () => {
			view.update("computerStopThinking", {});

			expect(spy).toHaveBeenCalledWith("Your turn")
		})

		test("should show 'You win!' when the player has won", () => {
			view.update("hasWinner", { winner: "player" });

			expect(spy).toHaveBeenCalledWith("You win!")
		})
	})
});