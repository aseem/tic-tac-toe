import { Component, Input, OnDestroy, OnInit } from '@angular/core';
import { GameService } from '../services/game.service';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-cell',
  templateUrl: './cell.component.html',
  styleUrls: ['./cell.component.css'],
})
export class CellComponent implements OnInit, OnDestroy {
  @Input() cellIndex: number = 0;
  cellValue: string = '';
  resetCellSubscription: Subscription;

  constructor(private gameService: GameService) {}

  ngOnInit(): void {
    this.resetCellSubscription = this.gameService.resetCell.subscribe(() => {
      this.cellValue = '';
    });
  }

  ngOnDestroy(): void {
    this.resetCellSubscription.unsubscribe();
  }

  cellClicked() {
    if (this.cellValue != '' || this.gameService.gameOver) {
      console.log('Cell #' + this.cellIndex + ' has already been played');
      return;
    }

    this.cellValue = this.gameService.getNextValue(this.cellIndex);
  }
}
