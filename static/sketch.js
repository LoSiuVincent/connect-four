import { Game } from "./game.js";

const CELL_SIZE = 100;

const game = new Game();
game.run()

window.game = game;