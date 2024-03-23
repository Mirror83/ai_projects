const PLAYER_ONE_TURN = 0;
const PLAYER_TWO_TURN = 1;

const PLAYER_ONE_TOKEN = "X";
const PLAYER_TWO_TOKEN = "O";
const EMPTY_CELL_TOKEN = "";

const PLAYER_ONE_WIN_STATE = "player_one_win";
const PLAYER_TWO_WIN_STATE = "player_two_win";
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

function matches(
  board,
  indexOne,
  indexTwo,
  indexThree,
  token = EMPTY_CELL_TOKEN
) {
  let isTokenMatched = false;

  if (token === EMPTY_CELL_TOKEN) {
    // This is for checking a general win
    isTokenMatched =
      board[indexOne] != token &&
      board[indexTwo] != token &&
      board[indexThree] != token;
  } else {
    isTokenMatched =
      board[indexOne] == token &&
      board[indexTwo] == token &&
      board[indexThree] == token;
  }

  return (
    board[indexOne] === board[indexTwo] &&
    board[indexOne] === board[indexThree] &&
    board[indexTwo] === board[indexThree] &&
    isTokenMatched
  );
}

function firstRowMatches(board, token = EMPTY_CELL_TOKEN) {
  return matches(board, 0, 1, 2, token);
}

function secondRowMatches(board, token = EMPTY_CELL_TOKEN) {
  return matches(board, 3, 4, 5, token);
}

function thirdRowMatches(board, token = EMPTY_CELL_TOKEN) {
  return matches(board, 6, 7, 8, token);
}

function firstColumnMatches(board, token = EMPTY_CELL_TOKEN) {
  return matches(board, 0, 3, 6, token);
}

function secondColumnMatches(board, token = EMPTY_CELL_TOKEN) {
  return matches(board, 1, 4, 7, token);
}

function thirdColumnMatches(board, token = EMPTY_CELL_TOKEN) {
  return matches(board, 2, 5, 8, token);
}

function diagonalFromZeroMatches(board, token = EMPTY_CELL_TOKEN) {
  return matches(board, 0, 4, 8, token);
}

function diagonalFromTwoMatches(board, token = EMPTY_CELL_TOKEN) {
  return matches(board, 2, 4, 6, token);
}

function updateTurn(turn) {
  turn = (turn + 1) % 2;
  turnIndicator.textContent = turn + 1;

  return turn;
}

function isWin(board, token = EMPTY_CELL_TOKEN) {
  return (
    firstRowMatches(board, token) ||
    secondRowMatches(board, token) ||
    thirdRowMatches(board, token) ||
    firstColumnMatches(board, token) ||
    secondColumnMatches(board, token) ||
    thirdColumnMatches(board, token) ||
    diagonalFromZeroMatches(board, token) ||
    diagonalFromTwoMatches(board, token)
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
  if (isWin(board, PLAYER_ONE_TOKEN)) return PLAYER_ONE_WIN_STATE;
  else if (isWin(board, PLAYER_TWO_TOKEN)) return PLAYER_TWO_WIN_STATE;
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
  } else if (boardState === PLAYER_ONE_WIN_STATE) {
    alert(`Player 1 has won!`);
  } else if (boardState === PLAYER_TWO_WIN_STATE) {
    alert(`Player 2 has won!`);
  } else {
    alert("Game is a draw.");
  }
}

function minimax(board, depth, isMaximizingPlayer) {
  // Check if board is in a terminal state
  const boardState = checkBoard(board);

  if (boardState === DRAW_STATE) return 0;
}
