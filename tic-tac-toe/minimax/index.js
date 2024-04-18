import {
  evaluate,
  findBestMove,
  isMovesLeft,
  resetBoard,
  placeToken,
  unflatten,
  EMPTY,
  PLAYER_ONE_WIN,
  PLAYER_TWO_WIN,
} from "./utils.js";

const cells = document.querySelectorAll(".cell");
const playButton = document.querySelector("#play");

const dialog = document.querySelector("dialog");
const dialogParagraph = document.querySelector("dialog p");
const closeButton = document.querySelector("dialog button");
const playerIndicator = document.querySelector("#turn-indicator");

const modeRadioButtons = document.querySelectorAll("input[name=mode]");
const algorithmSelection = document.querySelector("#algorithm-selection");

const PLAYER_ONE_TURN = 0;

const PLAYER_VS_CPU_MODE = 2;
const CPU_VS_CPU_MODE = 3;

let turn = PLAYER_ONE_TURN;
let isPlaying = false;

let mode = PLAYER_VS_CPU_MODE;

let board = [
  [EMPTY, EMPTY, EMPTY],
  [EMPTY, EMPTY, EMPTY],
  [EMPTY, EMPTY, EMPTY],
];

modeRadioButtons.forEach((input) => {
  input.addEventListener("change", () => {
    const idAttribute = input.attributes.getNamedItem("id");

    if (idAttribute.value === "cpu-vs-cpu") {
      mode = CPU_VS_CPU_MODE;
      algorithmSelection.classList.remove("hidden");
    } else {
      mode = PLAYER_VS_CPU_MODE;
      algorithmSelection.classList.add("hidden");
    }

    console.log(mode);
  });
});

playButton.addEventListener("click", () => {
  if (!isPlaying) playCpuVsCpu();
});

cells.forEach((cell, i) => {
  cell.addEventListener("click", () => {
    // If cell is already populated, there is no need to populate it again
    if (cell.firstChild) return;

    handleCellClick(isPlaying, i);
  });
});

closeButton.addEventListener("click", () => {
  resetBoard(board, cells);

  turn = PLAYER_ONE_TURN;
  updatePlayerIndicator(playerIndicator, turn);
  isPlaying = false;

  dialog.close();
});

function handleCellClick(isPlaying, i) {
  if ((mode === CPU_VS_CPU_MODE && !isPlaying) || mode === PLAYER_VS_CPU_MODE) {
    // Check for game over states
    makeMovePlayer(i);
    if (checkGameOver()) return;

    if (mode === PLAYER_VS_CPU_MODE) {
      setTimeout(() => {
        makeMoveCPU();
        checkGameOver();
      }, 1000);
    }
  }
}

function displayResultDialog(text) {
  dialogParagraph.textContent = text;
  dialog.showModal();
}

function updateTurn() {
  turn = (turn + 1) % 2;
  updatePlayerIndicator(playerIndicator, turn);
}

function updatePlayerIndicator(playerIndicator, turn) {
  playerIndicator.textContent = turn + 1;
}

function makeMoveCPU() {
  const bestMove = findBestMove(board, turn);
  placeToken(board, cells, bestMove.row, bestMove.col, turn);

  updateTurn();
}

function makeMovePlayer(i) {
  const { row, col } = unflatten(i);
  placeToken(board, cells, row, col, turn);
  updateTurn();
}

function checkGameOver() {
  const score = evaluate(board);
  console.log(score);

  if (score === PLAYER_ONE_WIN) {
    displayResultDialog("Player one wins!");
    return true;
  } else if (score === PLAYER_TWO_WIN) {
    displayResultDialog("Player two wins");
    return true;
  }
  if (!isMovesLeft(board)) {
    displayResultDialog("Game is a draw");
    return true;
  }

  return false;
}

function playCpuVsCpu() {
  isPlaying = true;
  const intervalId = setInterval(() => {
    const score = evaluate(board);

    if (score === PLAYER_ONE_WIN) {
      displayResultDialog("Player one wins!");
      clearInterval(intervalId);
      return;
    } else if (score === PLAYER_TWO_WIN) {
      displayResultDialog("Player two wins");
      clearInterval(intervalId);
      return;
    } else if (!isMovesLeft(board)) {
      displayResultDialog("Game is a draw");
      clearInterval(intervalId);
      return;
    }

    makeMoveCPU();
  }, 1000);
}
