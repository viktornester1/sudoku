document.addEventListener('DOMContentLoaded', function() {
  const gameContainer = document.getElementById('game-container');
  const newGameButton = document.getElementById('new-game-btn');
  const difficultyLevel = document.getElementById('difficulty-level');
  const submitButton = document.getElementById('submit-game-btn');

  let boardState = [];
  let solution = [];
  let startTime;

  function renderBoard(board) {
    const table = gameContainer.querySelector('table');
    for (let row = 0; row < 9; row++) {
      for (let col = 0; col < 9; col++) {
        const cell = table.rows[row].cells[col].querySelector('input');
        cell.value = board[row][col] === 0 ? '' : board[row][col];
        cell.readOnly = board[row][col] !== 0;
      }
    }
  }

  function newGame() {
    startTime = new Date().getTime();

    // Fetch the new board and solution based on the selected difficulty
    fetch(`/game?difficulty=${difficultyLevel.value}`, {
      headers: {
        'Accept': 'application/json'
      }
    })
    .then(response => response.json())
    .then(data => {
      boardState = data.board;
      solution = data.solution;
      renderBoard(boardState);
    })
    .catch(error => {
      console.error('Error:', error);
    });
  }

  function submitGame() {
    const timeElapsed = new Date().getTime() - startTime;
    const completed = JSON.stringify(boardState) === JSON.stringify(solution);

    const formData = {
      difficulty: difficultyLevel.value,
      board: boardState.flat().join(','), // Convert boardState to a comma-separated string
      time_taken: timeElapsed / 1000,
      completed: completed
    };

    fetch('/game', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify(formData)
    })
      .then(response => {
        if (response.ok) {
          alert('Game submitted successfully!');
          newGame();
        } else {
          alert('Failed to submit game. Please try again.');
        }
      })
      .catch(error => {
        console.error('Error:', error);
      });
  }

  // Add event listeners
  newGameButton.addEventListener('click', newGame);
  difficultyLevel.addEventListener('change', newGame);
  submitButton.addEventListener('click', submitGame);

  // Initialize the game
  newGame();

  // Handle user input
  gameContainer.addEventListener('input', (event) => {
    const cell = event.target;
    const row = cell.parentNode.parentNode.rowIndex;
    const col = cell.parentNode.cellIndex;
    const value = parseInt(cell.value) || 0;

    if (!isNaN(value) && value >= 0 && value <= 9) {
      boardState[row][col] = value;
    } else {
      cell.value = '';
      boardState[row][col] = 0;
    }
  });
});