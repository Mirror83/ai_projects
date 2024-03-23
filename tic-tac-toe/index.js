const PLAYER_ONE_TURN = 0;
const PLAYER_TWO_TURN = 1;

const PLAYER_ONE_TOKEN = "X";
const PLAYER_TWO_TOKEN = "O";
const EMPTY_CELL_TOKEN = "";

const WIN_STATE = "win";
const DRAW_STATE = "draw";
const PLAY_STATE = "play";

function clearBoard(board) {
  for (let i = 0; i < 9; i++) {
    board.push(EMPTY_CELL_TOKEN);
  }

  return [...board];
}

function isAvailable(board, index) {
  return board[index] === EMPTY_CELL_TOKEN;
}

function placeToken(board, index) {
  if (!isAvailable(board, index)) return [...board];

  if (turn === PLAYER_ONE_TURN) {
    board[index] = PLAYER_ONE_TOKEN;
  } else {
    board[index] = PLAYER_TWO_TOKEN;
  }

  return [...board];
}

function placeTokenUi(board, index) {
  if (isAvailable(board, index)) return;

  if (cells[index].querySelector("span")) return;

  const tokenSpan = document.createElement("span");
  tokenSpan.innerText = board[index];

  cells[index].appendChild(tokenSpan);
}

function matches(board, indexOne, indexTwo, indexThree) {
  return (
    board[indexOne] === board[indexTwo] &&
    board[indexOne] === board[indexThree] &&
    board[indexTwo] === board[indexThree] &&
    board[indexOne] != EMPTY_CELL_TOKEN &&
    board[indexTwo] != EMPTY_CELL_TOKEN &&
    board[indexThree] != EMPTY_CELL_TOKEN
  );
}

function firstRowMatches(board) {
  return matches(board, 0, 1, 2);
}

function secondRowMatches(board) {
  return matches(board, 3, 4, 5);
}

function thirdRowMatches(board) {
  return matches(board, 6, 7, 8);
}

function firstColumnMatches(board) {
  return matches(board, 0, 3, 6);
}

function secondColumnMatches(board) {
  return matches(board, 1, 4, 7);
}

function thirdColumnMatches(board) {
  return matches(board, 2, 5, 8);
}

function diagonalFromZeroMatches(board) {
  return matches(board, 0, 4, 8);
}

function diagonalFromTwoMatches(board) {
  return matches(board, 2, 4, 6);
}

function updateTurn(turn) {
  turn = (turn + 1) % 2;
  turnIndicator.textContent = turn + 1;

  return turn;
}

function isWin(board) {
  return (
    firstRowMatches(board) ||
    secondRowMatches(board) ||
    thirdRowMatches(board) ||
    firstColumnMatches(board) ||
    secondColumnMatches(board) ||
    thirdColumnMatches(board) ||
    diagonalFromZeroMatches(board) ||
    diagonalFromTwoMatches(board)
  );
}

function isDraw(board) {
  // Assume that the current board state does not contain a win false
  // Just checks if the board is filled
  for (const token of board) {
    if (token == EMPTY_CELL_TOKEN) return false;
  }

  return true;
}

function checkBoard(board) {
  if (isWin(board)) return WIN_STATE;
  else if (isDraw(board)) return DRAW_STATE;
  else return PLAY_STATE;
}

function possibleBoards(board) {
  const boards = [];

  for (let index in board) {
    const new_board = [...board];
    if (!isAvailable(new_board, index)) continue;

    boards.push(placeToken(new_board, index));
  }

  return boards;
}

const cells = document.querySelectorAll(".cell");
const turnIndicator = document.querySelector("#turn-indicator");
let turn = PLAYER_ONE_TURN;

let board = [];

board = clearBoard(board);
let boardState = PLAY_STATE;

const intervalId = setInterval(() => {
  const index = Math.round(Math.random() * 8);
  game(board, index);
}, 1000);

function game(board, index) {
  if (boardState != PLAY_STATE) {
    clearInterval(intervalId);
    return;
  }

  if (!isAvailable(board, index)) return;

  board = placeToken(board, index);

  placeTokenUi(board, index);

  console.log(board);

  boardState = checkBoard(board);

  if (boardState === PLAY_STATE) {
    turn = updateTurn(turn);
  } else if (boardState === WIN_STATE) {
    alert(`Player ${turn + 1} has won!`);
  } else {
    alert("Game is a draw.");
  }
}
