import { Component, OnInit, OnDestroy } from '@angular/core';
import { Subscription } from 'rxjs';
import { GameService } from './services/game.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
})
export class AppComponent implements OnInit, OnDestroy {
  title = 'tic-tac-toe';
  winningCells = [false, false, false, false, false, false, false, false];
  private winnerSubscription: Subscription;
  private resetCellSubscription: Subscription;

  constructor(private gameService: GameService) {}

  ngOnInit(): void {
    this.winnerSubscription = this.gameService.winnerUpdated.subscribe(
      (winningCells: number[]) => {
        console.log('Winning cells: ' + winningCells);
        winningCells.map((v) => {
          this.winningCells[v] = true;
        });
      }
    );
    this.resetCellSubscription = this.gameService.resetCell.subscribe(() => {
      this.winningCells.forEach((value, index) => {
        this.winningCells[index] = false;
      });
    });
  }

  ngOnDestroy(): void {
    this.winnerSubscription.unsubscribe();
  }

  restartGame() {
    this.gameService.resetGame();
  }
}
