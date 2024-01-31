export class Server {
    constructor(baseURL = "") {
        this.baseURL = baseURL;
    }

    async getComputerMove(encodedBoard) {
        const response = await fetch(`${this.baseURL}/predict`, { method: "POST", body: encodedBoard });
        const data = await response.json();
        return data.move;
    }
}