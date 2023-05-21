import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppComponent } from './app.component';
import { CellComponent } from './cell/cell.component';
import { GameService } from './services/game.service';

@NgModule({
  declarations: [AppComponent, CellComponent],
  imports: [BrowserModule],
  providers: [GameService],
  bootstrap: [AppComponent],
})
export class AppModule {}
