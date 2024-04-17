// Most of the code is from this site: https://www.geeksforgeeks.org/finding-optimal-move-in-tic-tac-toe-using-minimax-algorithm-in-game-theory/
// However, I modified the dirver code and the findBestMove function to support
// two computer players

class Move {
  constructor() {
    let row, col;
  }
}

export const PLAYER = "x";
export const OPPONENT = "o";
export const EMPTY = "_";

export const DRAW = 0;
export const PLAYER_ONE_WIN = 10;
export const PLAYER_TWO_WIN = -10;

// This function returns true if there are moves
// remaining on the board. It returns false if
// there are no moves left to play.
export function isMovesLeft(board) {
  for (let i = 0; i < 3; i++)
    for (let j = 0; j < 3; j++) if (board[i][j] == EMPTY) return true;

  return false;
}

// This is the evaluation function as discussed
// in the previous article ( http://goo.gl/sJgv68 )
export function evaluate(b) {
  // Checking for Rows for X or O victory.
  for (let row = 0; row < 3; row++) {
    if (b[row][0] == b[row][1] && b[row][1] == b[row][2]) {
      if (b[row][0] == PLAYER) return PLAYER_ONE_WIN;
      else if (b[row][0] == OPPONENT) return PLAYER_TWO_WIN;
    }
  }

  // Checking for Columns for X or O victory.
  for (let col = 0; col < 3; col++) {
    if (b[0][col] == b[1][col] && b[1][col] == b[2][col]) {
      if (b[0][col] == PLAYER) return PLAYER_ONE_WIN;
      else if (b[0][col] == OPPONENT) return PLAYER_TWO_WIN;
    }
  }

  // Checking for Diagonals for X or O victory.
  if (b[0][0] == b[1][1] && b[1][1] == b[2][2]) {
    if (b[0][0] == PLAYER) return PLAYER_ONE_WIN;
    else if (b[0][0] == OPPONENT) return PLAYER_TWO_WIN;
  }

  if (b[0][2] == b[1][1] && b[1][1] == b[2][0]) {
    if (b[0][2] == PLAYER) return PLAYER_ONE_WIN;
    else if (b[0][2] == OPPONENT) return PLAYER_TWO_WIN;
  }

  // Else if none of them have
  // won then return 0
  return DRAW;
}

// This is the minimax function. It
// considers all the possible ways
// the game can go and returns the
// value of the board
function minimax(board, depth, isMax) {
  let score = evaluate(board);

  // If Maximizer has won the game
  // return his/her evaluated score
  if (score == PLAYER_ONE_WIN) return score;

  // If Minimizer has won the game
  // return his/her evaluated score
  if (score == PLAYER_TWO_WIN) return score;

  // If there are no more moves and
  // no winner then it is a tie
  if (isMovesLeft(board) == false) return DRAW;

  // If this maximizer's move
  if (isMax) {
    let best = -1000;

    // Traverse all cells
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        // Check if cell is empty
        if (board[i][j] == EMPTY) {
          // Make the move
          board[i][j] = PLAYER;

          // Call minimax recursively
          // and choose the maximum value
          best = Math.max(best, minimax(board, depth + 1, !isMax));

          // Undo the move
          board[i][j] = EMPTY;
        }
      }
    }
    return best;
  }

  // If this minimizer's move
  else {
    let best = 1000;

    // Traverse all cells
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        // Check if cell is empty
        if (board[i][j] == EMPTY) {
          // Make the move
          board[i][j] = OPPONENT;

          // Call minimax recursively and
          // choose the minimum value
          best = Math.min(best, minimax(board, depth + 1, !isMax));

          // Undo the move
          board[i][j] = EMPTY;
        }
      }
    }
    return best;
  }
}

// This will return the best possible
// move for the player
export function findBestMove(board, currentTurn) {
  if (currentTurn === 0) {
    let bestVal = -1000;
    let bestMove = new Move();
    bestMove.row = -1;
    bestMove.col = -1;

    // Traverse all cells, evaluate
    // minimax function for all empty
    // cells. And return the cell
    // with optimal value.
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        // Check if cell is empty
        if (board[i][j] == EMPTY) {
          // Make the move
          board[i][j] = PLAYER;

          // compute evaluation function
          // for this move.
          let moveVal = minimax(board, 0, false);

          // Undo the move
          board[i][j] = EMPTY;

          // If the value of the current move
          // is more than the best value, then
          // update best
          if (moveVal > bestVal) {
            bestMove.row = i;
            bestMove.col = j;
            bestVal = moveVal;
          }
        }
      }
    }

    return bestMove;
  } else {
    let bestVal = 1000;
    let bestMove = new Move();
    bestMove.row = -1;
    bestMove.col = -1;

    // Traverse all cells, evaluate
    // minimax function for all empty
    // cells. And return the cell
    // with optimal value.
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        // Check if cell is empty
        if (board[i][j] == EMPTY) {
          // Make the move
          board[i][j] = OPPONENT;

          // compute evaluation function
          // for this move.
          let moveVal = minimax(board, 0, true);

          // Undo the move
          board[i][j] = EMPTY;

          // If the value of the current move
          // is more than the best value, then
          // update best
          if (moveVal < bestVal) {
            bestMove.row = i;
            bestMove.col = j;
            bestVal = moveVal;
          }
        }
      }
    }

    return bestMove;
  }
}

export function flatten(row, col) {
  const flatIndex = row * 3 + col;

  return flatIndex;
}

export function unflatten(i) {
  const row = Math.floor(i / 3);
  const col = i % 3;

  return { row, col };
}

export function placeToken(board, cells, row, col, turn) {
  board[row][col] = turn === 0 ? PLAYER : OPPONENT;
  placeTokenUi(board, cells, row, col);
}

export function placeTokenUi(board, cells, row, col) {
  const flatIndex = flatten(row, col);

  const span = document.createElement("span");
  span.textContent = board[row][col];
  cells[flatIndex].appendChild(span);
}

export function resetBoard(board, cells) {
  for (let i = 0; i < 3; i++) {
    for (let j = 0; j < 3; j++) {
      board[i][j] = EMPTY;
    }
  }
  clearTokensUi(cells);
}

export function clearTokensUi(cells) {
  for (let cell of cells) {
    if (cell.firstChild) cell.removeChild(cell.firstChild);
  }
}
