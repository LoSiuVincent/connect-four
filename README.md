# Connect Four with MCTS Bot

Welcome to the Connect Four with MCTS Bot repository. This game implementation is a modern twist on the classic two-player connection game. In this version, you'll be pitted against a powerful AI opponent powered by a Monte Carlo Tree Search (MCTS) algorithm, known for its strength in strategic gameplay.

## Getting Started

These instructions will help you get a copy of the project up and running on your local machine for both development and gameplay.

### Prerequisites

Before starting, make sure you have the following installed:

- Git
- Docker
- Docker Compose

### Installing

#### Option 1: Using Docker Compose

1. Clone the repository:

    ```sh
    git clone https://github.com/LoSiuVincent/connect-four.git
    ```

2. Navigate to the project directory:

    ```sh
    cd connect-four
    ```

3. Launch the game server using Docker Compose:

    ```sh
    docker-compose up
    ```

After executing the command, the game server will be active, and you can access the game through your web browser by visiting the localhost port specified by your Docker setup (default port is 8000).

#### Option 2: Using Poetry and Make

If you prefer not to use Docker, you can set up your project using Poetry, which is a tool for dependency management and packaging in Python. Additionally, you can use `make` to run predefined tasks such as running the server.

1. Clone the repository if you haven't already:

    ```sh
    git clone https://github.com/LoSiuVincent/connect-four.git
    ```

2. Navigate to the project directory:

    ```sh
    cd connect-four
    ```

3. Install Poetry if it's not already installed. You can install it by following the instructions on the [official Poetry website](https://python-poetry.org/docs/).

4. Install the project dependencies using Poetry:

    ```sh
    poetry install
    ```

5. Once the dependencies are installed, you can run the game server:

    ```sh
    make run-prod
    ```

After executing the command, the game server will be active, and you can access the game through your web browser by visiting the localhost port specified in your server setup (default port is 8000).

## Gameplay

To play the game, simply open it in your web browser after starting the server. You will take on the role of the first player, competing against the AI bot. Your objective is to connect four of your colored discs in a row—horizontally, vertically, or diagonally—before the MCTS bot achieves the same.

The AI bot is powered by the Monte Carlo Tree Search (MCTS) algorithm, which provides a formidable and dynamic challenge, ensuring each game is a unique strategic encounter. Test your skills and see if you can outmaneuver the AI.

To restart the game at any time, refresh the page in your web browser. This will reset the board and give you a fresh start to try new strategies against the AI opponent. Enjoy the game and good luck!

## Contributing

Thank you for your interest in the Connect Four with MCTS Bot project. At this time, the project is considered complete, and I am not looking to add more features or accept contributions. The repository is shared for educational purposes and as a portfolio piece.

Feel free to fork the project and experiment on your own. However, please be aware that pull requests will not be merged into this project.

## License

This project is open-sourced under the MIT License. See the LICENSE file for more information.
