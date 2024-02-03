import { Server } from "server.js"
import { jest, expect, describe, test } from "@jest/globals";

test("getComputerMove should return an integer", async () => {
    const server = new Server();
    jest.spyOn(global, "fetch").mockResolvedValue({
        json: jest.fn().mockResolvedValue({ move: 2 }),
    });

    const result = await server.getComputerMove("PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE");

    expect(result).toEqual(2);
})

describe("when send request", () => {
    test("should send test request by default", async () => {
        const server = new Server();
        const fetchSpy = jest.spyOn(global, "fetch");

        await server.getComputerMove("PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE")

        expect(fetchSpy).toHaveBeenCalledWith("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ board: "PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE", test: true })
        });
    })

    test("should send non test request when specified", async () => {
        const server = new Server("", false);
        const fetchSpy = jest.spyOn(global, "fetch");

        await server.getComputerMove("PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE")

        expect(fetchSpy).toHaveBeenCalledWith("/predict", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ board: "PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE", test: false })
        });
    })
})