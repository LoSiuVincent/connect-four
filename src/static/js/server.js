export class Server {
    async getComputerMove(encodedBoard) {
        const response = await fetch("/predict", { method: "POST", body: encodedBoard });
        const data = await response.json();
        return data.move;
    }
}