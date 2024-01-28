import { Game } from "./game.js";

const CELL_SIZE = 100;

const game = new Game(CELL_SIZE);
game.run()

window.game = game;