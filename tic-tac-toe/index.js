const cells = document.querySelectorAll(".cell");
const turnIndicator = document.querySelector("#turn-indicator");

let turn = 0;
const PLAYER_ONE_TOKEN = "X";
const PLAYER_TWO_TOKEN = "O";
const EMPTY_CELL_TOKEN = "";

const WIN_STATE = "win";
const DRAW_STATE = "draw";
const PLAY_STATE = "play";

function content(cell) {
  const span = cell.querySelector("span");
  if (!span) return EMPTY_CELL_TOKEN;

  return span.textContent;
}

function matches(indexOne, indexTwo, indexThree) {
  return (
    content(cells[indexOne]) === content(cells[indexTwo]) &&
    content(cells[indexOne]) === content(cells[indexThree]) &&
    content(cells[indexTwo]) === content(cells[indexThree]) &&
    content(cells[indexOne]) != EMPTY_CELL_TOKEN &&
    content(cells[indexTwo]) != EMPTY_CELL_TOKEN &&
    content(cells[indexThree]) != EMPTY_CELL_TOKEN
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
  for (const cell of cells) {
    if (!cell.querySelector("span")) return false;
  }

  return true;
}

function isAvailable(index) {
  return cells[index].querySelector("span");
}

function checkBoard() {
  if (isWin()) {
    return WIN_STATE;
  } else if (isDraw()) return DRAW_STATE;
  else return PLAY_STATE;
}

cells.forEach((cell) => {
  cell.addEventListener("click", () => {
    console.log(turn);

    if (cell.querySelector("span")) {
      return;
    }

    const tokenSpan = document.createElement("span");
    if (turn == 0) {
      tokenSpan.innerText = PLAYER_ONE_TOKEN;
    } else {
      tokenSpan.innerText = PLAYER_TWO_TOKEN;
    }

    cell.appendChild(tokenSpan);

    const boardState = checkBoard();

    if (boardState === PLAY_STATE) {
      turn = (turn + 1) % 2;
      turnIndicator.textContent = turn + 1;
    } else if (boardState === WIN_STATE) {
      alert(`Player ${turn + 1} has won!`);
    } else {
      alert("Game is a draw.");
    }
  });
});
