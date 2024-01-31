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

test("server should call fetch", async () => {
    const server = new Server();
    const fetchSpy = jest.spyOn(global, "fetch");

    const result = await server.getComputerMove("PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE");

    expect(fetchSpy).toHaveBeenCalledWith("/predict", { method: "POST", body: "PEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE|EEEEEEE" });
})