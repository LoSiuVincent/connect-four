import { Graphics } from "./graphics.js";
import { Subject } from "./subject.js";

export class p5View {
	constructor(game, p5, cellLength) {
		this._game = game;
		this._p5 = p5;
		this._graphics = new Graphics(p5, cellLength, game);
		this._subject = new Subject();

		this._p5.mouseClicked = () => {
			this.notify("mouseClick", { x: this._p5.mouseX, y: this._p5.mouseY });
		};
		this._game.addListener("computerStartThinking", this);
		this._game.addListener("computerStopThinking", this);
		this._game.addListener("hasWinner", this);
		this._game.addListener("draw", this);
	}

	getCellLength() {
		return this._graphics.getCellLength();
	}

	getCanvasWidth() {
		return this._graphics.getCanvasWidth();
	}

	getCanvasHeight() {
		return this._graphics.getCanvasHeight();
	}

	isInsideCanvas(x, y) {
		return 0 <= x && x <= this._graphics.getCanvasWidth() && 0 <= y && y <= this._graphics.getCanvasHeight();
	}

	changeStateText(text) {
		$("p").text(text);
	}

	async update(event, data) {
		if (event === "computerStartThinking") {
			this.changeStateText("Thinking ...");
		} else if (event === "computerStopThinking") {
			this.changeStateText("Your turn");
		} else if (event === "hasWinner") {
			if (data.winner === "player") {
				this.changeStateText("You win!");
			} else {
				this.changeStateText("You lose, try again!");
			}
		} else if (event === "draw") {
			this.changeStateText("Draw!");
		}
	}

	addListener(event, listener) {
		this._subject.addListener(event, listener);
	}

	async notify(event, data) {
		return this._subject.notify(event, data);
	}

	setup() {
		this._graphics.setup();
	}

	draw() {
		this._graphics.draw();
	}
}