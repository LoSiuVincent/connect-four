import { p5View } from "view.js";
import { jest, expect } from "@jest/globals";

test("View has the correct cell length", () => {
	const dummyObject = {};
	const view = new p5View(dummyObject, dummyObject, 100);

	expect(view.getCellLength()).toBe(100);
});

test("View has the correct canvas width", () => {
	const dummyObject = {};
	const view = new p5View(dummyObject, dummyObject, 100);
	const biggerView = new p5View(dummyObject, dummyObject, 150);

	expect(view.getCanvasWidth()).toBe(700);
	expect(biggerView.getCanvasWidth()).toBe(1050);
});

test("View has the correct canvas height", () => {
	const dummyObject = {};
	const view = new p5View(dummyObject, dummyObject, 100);
	const biggerView = new p5View(dummyObject, dummyObject, 150);

	expect(view.getCanvasHeight()).toBe(800);
	expect(biggerView.getCanvasHeight()).toBe(1200);
});

test("View should notify listeners when they subscribe to it", () => {
	const dummyObject = {};
	const view = new p5View(dummyObject, dummyObject, dummyObject);
	const callbackOne = jest.fn();
	const callbackTwo = jest.fn();
	const callbackThree = jest.fn();
	view.addListener("mouseClick", callbackOne);
	view.addListener("mouseClick", callbackTwo);
	view.addListener("otherEvent", callbackThree);

	view.notify("mouseClick", { x: 10, y: 10 });

	expect(callbackOne).toHaveBeenCalledWith({ x: 10, y: 10 });
	expect(callbackTwo).toHaveBeenCalledWith({ x: 10, y: 10 });
	expect(callbackThree).not.toHaveBeenCalled();
});
