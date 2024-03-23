// Javascript program to find the
// next optimal move for a player
class Move {
  constructor() {
    let row, col;
  }
}

let player = "x",
  opponent = "o";

// This function returns true if there are moves
// remaining on the board. It returns false if
// there are no moves left to play.
function isMovesLeft(board) {
  for (let i = 0; i < 3; i++)
    for (let j = 0; j < 3; j++) if (board[i][j] == "_") return true;

  return false;
}

// This is the evaluation function as discussed
// in the previous article ( http://goo.gl/sJgv68 )
function evaluate(b) {
  // Checking for Rows for X or O victory.
  for (let row = 0; row < 3; row++) {
    if (b[row][0] == b[row][1] && b[row][1] == b[row][2]) {
      if (b[row][0] == player) return +10;
      else if (b[row][0] == opponent) return -10;
    }
  }

  // Checking for Columns for X or O victory.
  for (let col = 0; col < 3; col++) {
    if (b[0][col] == b[1][col] && b[1][col] == b[2][col]) {
      if (b[0][col] == player) return +10;
      else if (b[0][col] == opponent) return -10;
    }
  }

  // Checking for Diagonals for X or O victory.
  if (b[0][0] == b[1][1] && b[1][1] == b[2][2]) {
    if (b[0][0] == player) return +10;
    else if (b[0][0] == opponent) return -10;
  }

  if (b[0][2] == b[1][1] && b[1][1] == b[2][0]) {
    if (b[0][2] == player) return +10;
    else if (b[0][2] == opponent) return -10;
  }

  // Else if none of them have
  // won then return 0
  return 0;
}

// This is the minimax function. It
// considers all the possible ways
// the game can go and returns the
// value of the board
function minimax(board, depth, isMax) {
  let score = evaluate(board);

  // If Maximizer has won the game
  // return his/her evaluated score
  if (score == 10) return score;

  // If Minimizer has won the game
  // return his/her evaluated score
  if (score == -10) return score;

  // If there are no more moves and
  // no winner then it is a tie
  if (isMovesLeft(board) == false) return 0;

  // If this maximizer's move
  if (isMax) {
    let best = -1000;

    // Traverse all cells
    for (let i = 0; i < 3; i++) {
      for (let j = 0; j < 3; j++) {
        // Check if cell is empty
        if (board[i][j] == "_") {
          // Make the move
          board[i][j] = player;

          // Call minimax recursively
          // and choose the maximum value
          best = Math.max(best, minimax(board, depth + 1, !isMax));

          // Undo the move
          board[i][j] = "_";
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
        if (board[i][j] == "_") {
          // Make the move
          board[i][j] = opponent;

          // Call minimax recursively and
          // choose the minimum value
          best = Math.min(best, minimax(board, depth + 1, !isMax));

          // Undo the move
          board[i][j] = "_";
        }
      }
    }
    return best;
  }
}

// This will return the best possible
// move for the player
function findBestMove(board, currentTurn) {
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
        if (board[i][j] == "_") {
          // Make the move
          board[i][j] = player;

          // compute evaluation function
          // for this move.
          let moveVal = minimax(board, 0, false);

          // Undo the move
          board[i][j] = "_";

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
        if (board[i][j] == "_") {
          // Make the move
          board[i][j] = opponent;

          // compute evaluation function
          // for this move.
          let moveVal = minimax(board, 0, true);

          // Undo the move
          board[i][j] = "_";

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

// Driver code
let board = [
  ["_", "_", "_"],
  ["_", "_", "_"],
  ["_", "_", "_"],
];

let turn = 0;

const cells = document.querySelectorAll(".cell");

const intervalId = setInterval(() => {
  let score = evaluate(board);

  if (score === 10) {
    alert("Player one wins!");
    clearInterval(intervalId);
    return;
  } else if (score === -10) {
    alert("Player two wins");
    clearInterval(intervalId);
    return;
  }
  if (!isMovesLeft(board)) {
    alert("Game is a draw");
    clearInterval(intervalId);
    return;
  }

  let bestMove = findBestMove(board, turn);
  console.log(bestMove);
  board[bestMove.row][bestMove.col] = turn === 0 ? player : opponent;

  const flatIndex = bestMove.col * 3 + bestMove.row;
  console.log(flatIndex);

  const span = document.createElement("span");
  span.textContent = board[bestMove.row][bestMove.col];
  cells[flatIndex].appendChild(span);
  turn = (turn + 1) % 2;
}, 1000);

// Most of the code is from this site: https://www.geeksforgeeks.org/finding-optimal-move-in-tic-tac-toe-using-minimax-algorithm-in-game-theory/
// However, I modified the dirver code and the findBestMove function to support
// two computer players
