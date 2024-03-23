const PLAYER_ONE_TURN = 0;
const PLAYER_TWO_TURN = 1;

const PLAYER_ONE_TOKEN = "X";
const PLAYER_TWO_TOKEN = "O";
const EMPTY_CELL_TOKEN = "";

const WIN_STATE = "win";
const DRAW_STATE = "draw";
const PLAY_STATE = "play";

function clearBoard() {
  for (var i = 0; i < 9; i++) {
    board.push(EMPTY_CELL_TOKEN);
  }
}

function isAvailable(index) {
  return board[index] === EMPTY_CELL_TOKEN;
}

function placeToken(index) {
  if (!isAvailable(index)) return;

  if (turn === PLAYER_ONE_TURN) {
    board[index] = PLAYER_ONE_TOKEN;
  } else {
    board[index] = PLAYER_TWO_TOKEN;
  }

  placeTokenUi(index);
}

function placeTokenUi(index) {
  const tokenSpan = document.createElement("span");
  if (turn === PLAYER_ONE_TURN) {
    tokenSpan.innerText = PLAYER_ONE_TOKEN;
  } else {
    tokenSpan.innerText = PLAYER_TWO_TOKEN;
  }

  cells[index].appendChild(tokenSpan);
}

function matches(indexOne, indexTwo, indexThree) {
  return (
    board[indexOne] === board[indexTwo] &&
    board[indexOne] === board[indexThree] &&
    board[indexTwo] === board[indexThree] &&
    board[indexOne] != EMPTY_CELL_TOKEN &&
    board[indexTwo] != EMPTY_CELL_TOKEN &&
    board[indexThree] != EMPTY_CELL_TOKEN
  );
}

function firstRowMatches() {
  return matches(0, 1, 2);
}

function secondRowMatches() {
  return matches(3, 4, 5);
}

function thirdRowMatches() {
  return matches(6, 7, 8);
}

function firstColumnMatches() {
  return matches(0, 3, 6);
}

function secondColumnMatches() {
  return matches(1, 4, 7);
}

function thirdColumnMatches() {
  return matches(2, 5, 8);
}

function diagonalFromZeroMatches() {
  return matches(0, 4, 8);
}

function diagonalFromTwoMatches() {
  return matches(2, 4, 6);
}

function updateTurn() {
  turn = (turn + 1) % 2;
  turnIndicator.textContent = turn + 1;
}

function isWin() {
  return (
    firstRowMatches() ||
    secondRowMatches() ||
    thirdRowMatches() ||
    firstColumnMatches() ||
    secondColumnMatches() ||
    thirdColumnMatches() ||
    diagonalFromZeroMatches() ||
    diagonalFromTwoMatches()
  );
}

function isDraw() {
  // Assume that the current board state does not contain a win false
  // Just checks if the board is filled
  for (const token of board) {
    if (token == EMPTY_CELL_TOKEN) return false;
  }

  return true;
}

function checkBoard() {
  if (isWin()) return WIN_STATE;
  else if (isDraw()) return DRAW_STATE;
  else return PLAY_STATE;
}

const cells = document.querySelectorAll(".cell");
const turnIndicator = document.querySelector("#turn-indicator");
let turn = PLAYER_ONE_TURN;

const board = [];

clearBoard();

cells.forEach((cell, index) => {
  cell.addEventListener("click", () => {
    placeToken(index);

    const boardState = checkBoard();

    if (boardState === PLAY_STATE) {
      updateTurn();
    } else if (boardState === WIN_STATE) {
      alert(`Player ${turn + 1} has won!`);
    } else {
      alert("Game is a draw.");
    }
  });
});
