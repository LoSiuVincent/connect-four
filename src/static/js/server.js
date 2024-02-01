export class Server {
    constructor(baseURL = "") {
        this.baseURL = baseURL;
    }

    async getComputerMove(encodedBoard) {
        const response = await fetch(`${this.baseURL}/predict`, { method: "POST", headers: { "Content-Type": "text/plain" }, body: encodedBoard });
        const data = await response.json();
        return data.move;
    }
}