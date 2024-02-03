export class Server {
    constructor(baseURL = "", test = true) {
        this._baseURL = baseURL;
        this._test = test;
    }

    async getComputerMove(encodedBoard) {
        const response = await fetch(`${this._baseURL}/predict`, {
            method: "POST", headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ board: encodedBoard, test: this._test })
        });
        const data = await response.json();
        return data.move;
    }
}