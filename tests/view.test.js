import { p5View } from "../static/view.js";

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
