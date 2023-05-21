import { Subject } from 'rxjs';

export class GameService {
  private currentValue: string = 'X';
  private currentBoard: string[] = ['', '', '', '', '', '', '', '', ''];
  public gameOver: boolean = false;
  public winnerUpdated = new Subject();
  public resetCell = new Subject<void>();

  // Utilities
  private checkForWinner(): boolean {
    // Check rows
    for (let i = 0; i < 3; i++) {
      if (this.currentBoard[i * 3] !== '') {
        if (
          this.currentBoard[i * 3] === this.currentBoard[i * 3 + 1] &&
          this.currentBoard[i * 3] === this.currentBoard[i * 3 + 2]
        ) {
          this.winnerUpdated.next([i * 3, i * 3 + 1, i * 3 + 2]);
          return true;
        }
      }
    }

    // Check columns
    for (let i = 0; i < 3; i++) {
      if (this.currentBoard[i] !== '') {
        if (
          this.currentBoard[i] === this.currentBoard[i + 3] &&
          this.currentBoard[i] === this.currentBoard[i + 6]
        ) {
          this.winnerUpdated.next([i, i + 3, i + 6]);
          return true;
        }
      }
    }

    // Check diagonals
    if (this.currentBoard[4] !== '') {
      if (
        this.currentBoard[4] === this.currentBoard[0] &&
        this.currentBoard[4] === this.currentBoard[8]
      ) {
        this.winnerUpdated.next([0, 4, 8]);
        return true;
      }
    }
    if (this.currentBoard[4] !== '') {
      if (
        this.currentBoard[4] === this.currentBoard[2] &&
        this.currentBoard[4] === this.currentBoard[6]
      ) {
        this.winnerUpdated.next([2, 4, 6]);
        return true;
      }
    }

    return false;
  }

  // Public Methods

  public getNextValue(cellIndex: number) {
    let value = this.currentValue;
    this.currentBoard[cellIndex] = value;

    // check if game is over
    this.gameOver = this.checkForWinner();

    this.currentValue = this.currentValue === 'X' ? 'O' : 'X';
    return value;
  }

  public resetGame() {
    this.currentValue = 'X';
    this.currentBoard = ['', '', '', '', '', '', '', '', ''];
    this.gameOver = false;
    this.resetCell.next();
  }
}
