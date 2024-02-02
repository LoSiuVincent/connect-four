import { Game, make2DBoard } from "game.js";
import { test, expect, jest, describe } from "@jest/globals";

let game, mockServer;

beforeEach(() => {
	mockServer = { getComputerMove: jest.fn().mockResolvedValue(1) };
	game = new Game(mockServer);
})

test("create a Game object without problem", () => {
	expect(game).toBeDefined();
});

test("all cell should be emptied on start", () => {
	for (var i = 0; i < 6; i++) {
		for (var j = 0; j < 7; j++) {
			expect(game.getCellState(i, j)).toBe("empty");
		}
	}
});

test("drop multiple coins should stack up properly", () => {
	game.dropCoin(0);
	game.dropCoin(0);
	game.dropCoin(1);

	let expectedBoard = make2DBoard(6, 7);
	expectedBoard[0][0] = "player";
	expectedBoard[1][0] = "player";
	expectedBoard[0][1] = "player";
	expect(game._board).toEqual(expectedBoard);
});

test("drop a computer coin should change the cell state to 'computer'", () => {
	game.dropCoin(0, "computer");
	game.dropCoin(2, "computer");

	let expectedBoard = make2DBoard(6, 7);
	expectedBoard[0][0] = "computer";
	expectedBoard[0][2] = "computer";
	expect(game._board).toEqual(expectedBoard);
})

test("should encode board to correct string", () => {
	game.dropCoin(0);
	game.dropCoin(0, "computer");

	expect(game._encodeBoard()).toEqual("PEEEEEE|CEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE");
});

test("should ask the server for a computer move", () => {
	game.dropCoin(0);
	game.makeComputerMove();

	expect(mockServer.getComputerMove).toHaveBeenCalledWith("PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE")
})

test("getWinner returns empty string when there is no winner", () => {
	game.dropCoin(0);

	expect(game.getWinner()).toEqual("");
})

describe("notification when there is a winner", () => {
	test("should notify when player wins", () => {
		const spy = jest.spyOn(game, "notify");

		for (let i = 0; i < 3; i++) {
			game.dropCoin(0);
			game.dropCoin(1, "computer");
		}
		game.dropCoin(0);

		expect(spy).toHaveBeenCalledWith("hasWinner", { winner: "player" })
	})

	test("should notify when computer wins", () => {
		const spy = jest.spyOn(game, "notify");

		for (let i = 0; i < 3; i++) {
			game.dropCoin(0, "computer");
			game.dropCoin(1);
		}
		game.dropCoin(0, "computer");

		expect(spy).toHaveBeenCalledWith("hasWinner", { winner: "computer" })
	})
})

test("Game should notify listeners when they subscribe to it", () => {
	const listenerOne = { update: jest.fn() };
	const listenerTwo = { update: jest.fn() };
	const listenerThree = { update: jest.fn() };
	game.addListener("computerStartThinking", listenerOne);
	game.addListener("computerStopThinking", listenerTwo);
	game.addListener("otherEvent", listenerThree);

	game.notify("computerStartThinking");
	game.notify("computerStopThinking");

	expect(listenerOne.update).toHaveBeenCalledWith("computerStartThinking", {});
	expect(listenerTwo.update).toHaveBeenCalledWith("computerStopThinking", {});
	expect(listenerThree.update).not.toHaveBeenCalled();
});

describe("isComputerThinking", () => {
	test("should return true when it is not resolved", () => {
		game.makeComputerMove();

		expect(game.isComputerThinking()).toEqual(true);
	})

	test("should return false when it is resolved", async () => {
		const promise = game.makeComputerMove();
		expect(game.isComputerThinking()).toEqual(true);

		await promise;
		expect(game.isComputerThinking()).toEqual(false);
	})
})

describe("when player wins", () => {
	test("by four vertical coins", () => {
		game.dropCoin(3);
		game.dropCoin(2, "computer");
		game.dropCoin(3);
		game.dropCoin(2, "computer");
		game.dropCoin(3);
		game.dropCoin(2, "computer");
		game.dropCoin(3);

		expect(game.getWinner()).toEqual("player");
	})

	test("by four horizontal coins", () => {
		game.dropCoin(0);
		game.dropCoin(0, "computer");
		game.dropCoin(1);
		game.dropCoin(1, "computer");
		game.dropCoin(2);
		game.dropCoin(2, "computer");
		game.dropCoin(3);

		expect(game.getWinner()).toEqual("player");
	});

	test("by four diagonal coins (bottom left to top right)", () => {
		game.dropCoin(0);
		game.dropCoin(1, "computer");
		game.dropCoin(1);
		game.dropCoin(2, "computer");
		game.dropCoin(2);
		game.dropCoin(3, "computer");
		game.dropCoin(2);
		game.dropCoin(3, "computer");
		game.dropCoin(3);
		game.dropCoin(4, "computer");
		game.dropCoin(3);

		expect(game.getWinner()).toEqual("player");
	});

	test("by four off-diagonal coins (top left to bottom right)", () => {
		game.dropCoin(3);
		game.dropCoin(2, "computer");
		game.dropCoin(2);
		game.dropCoin(1, "computer");
		game.dropCoin(1);
		game.dropCoin(0, "computer");
		game.dropCoin(1);
		game.dropCoin(0, "computer");
		game.dropCoin(0);
		game.dropCoin(3, "computer");
		game.dropCoin(0);

		expect(game.getWinner()).toEqual("player");
	});
})

describe("when computer wins", () => {
	test("by four vertical coins", () => {
		game.dropCoin(3, "computer");
		game.dropCoin(2);
		game.dropCoin(3, "computer");
		game.dropCoin(2);
		game.dropCoin(3, "computer");
		game.dropCoin(2);
		game.dropCoin(3, "computer");

		expect(game.getWinner()).toEqual("computer");
	});

	test("by four horizontal coins", () => {
		game.dropCoin(0, "computer");
		game.dropCoin(0);
		game.dropCoin(1, "computer");
		game.dropCoin(1);
		game.dropCoin(2, "computer");
		game.dropCoin(2);
		game.dropCoin(3, "computer");

		expect(game.getWinner()).toEqual("computer");
	});

	test("by four diagonal coins (bottom left to top right)", () => {
		game.dropCoin(0, "computer");
		game.dropCoin(1);
		game.dropCoin(1, "computer");
		game.dropCoin(2);
		game.dropCoin(2, "computer");
		game.dropCoin(3);
		game.dropCoin(2, "computer");
		game.dropCoin(3);
		game.dropCoin(3, "computer");
		game.dropCoin(4);
		game.dropCoin(3, "computer");

		expect(game.getWinner()).toEqual("computer");
	});

	test("by four off-diagonal coins (top left to bottom right)", () => {
		game.dropCoin(3, "computer");
		game.dropCoin(2);
		game.dropCoin(2, "computer");
		game.dropCoin(1);
		game.dropCoin(1, "computer");
		game.dropCoin(0);
		game.dropCoin(1, "computer");
		game.dropCoin(0);
		game.dropCoin(0, "computer");
		game.dropCoin(3);
		game.dropCoin(0, "computer");

		expect(game.getWinner()).toEqual("computer");
	});
});