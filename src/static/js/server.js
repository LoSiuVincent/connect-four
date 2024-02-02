export class Server {
    constructor(baseURL = "") {
        this._baseURL = baseURL;
    }

    async getComputerMove(encodedBoard) {
        const response = await fetch(`${this._baseURL}/predict`, { method: "POST", headers: { "Content-Type": "text/plain" }, body: encodedBoard });
        const data = await response.json();
        return data.move;
    }
}