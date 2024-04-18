// This game basically determines the best move for the AI player using minimax algorithm and alpha beta pruning
function bestMove() {
    // Initialize variables
    let bestScore = -Infinity; // Initialize bestScore as negative infinity
    let move; // Store the best move
    let alpha = -Infinity; // Initialize alpha as negative infinity for alpha-beta pruning
    let beta = Infinity;

    // Loop through all positions on the board
    for (let i = 0; i < 3; i++) {
        for (let j = 0; j < 3; j++) {
            // Check if the spot is available
            if (board[i][j] == '') {
                // Try the move
                board[i][j] = ai;
                // Calculate score using minimax algorithm with alpha-beta pruning
                let score = minimax(board, 0, false, alpha, beta);
                // Undo the move
                board[i][j] = '';
                // Update bestScore and move if the current move leads to a better score
                if (score > bestScore) {
                    bestScore = score;
                    move = { i, j };
                }
            }
        }
    }
    // Make the best move on the board
    board[move.i][move.j] = ai;
    // Switch to human player's turn
    currentPlayer = human;
}

// Scores for different game outcomes
let scores = {
    X: 10, // AI wins
    O: -10, // Human wins
    tie: 0 // Tie game
};

// Minimax algorithm with alpha-beta pruning
function minimax(board, depth, isMaximizing, alpha, beta) {
    // Check if a winner exists at this state
    let result = checkWinner();
    if (result !== null) {
        return scores[result]; // Return the score based on the winner
    }

    if (isMaximizing) {
        // Maximizing player's turn (AI)
        let bestScore = -Infinity; // Any move that the AI explores is better than the initial best Score
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                // Check if the spot is available
                if (board[i][j] == '') {
                    // Try the move for AI
                    board[i][j] = ai;
                    // Recursive call to minimax for the next level
                    let score = minimax(board, depth + 1, false, alpha, beta);
                    // Undo the move
                    board[i][j] = '';
                    // Update bestScore and alpha
                    bestScore = Math.max(score, bestScore);
                    alpha = Math.max(alpha, bestScore);
                    // Alpha-beta pruning
                    if (beta <= alpha) {
                        break; // Beta cut-off
                    }
                }
            }
        }
        return bestScore; // Return the best score for maximizing player
    } else {
        // Minimizing player's turn (Human)
        let bestScore = Infinity; // Any move by the human will have a lower score than the initial bestScore
        for (let i = 0; i < 3; i++) {
            for (let j = 0; j < 3; j++) {
                // Check if the spot is available
                if (board[i][j] == '') {
                    // Try the move for Human
                    board[i][j] = human;
                    // Recursive call to minimax for the next level
                    let score = minimax(board, depth + 1, true, alpha, beta);
                    // Undo the move
                    board[i][j] = '';
                    // Update bestScore and beta
                    bestScore = Math.min(score, bestScore);
                    beta = Math.min(beta, bestScore);
                    // Alpha-beta pruning
                    if (beta <= alpha) {
                        break; // Alpha cut-off
                    }
                }
            }
        }
        return bestScore; // Return the best score for minimizing player
    }
}
