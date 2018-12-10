import { Component, OnDestroy, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import {interval} from 'rxjs';

@Component({
  selector: 'app-coffee-preparation',
  templateUrl: './coffee-preparation.component.html',
  styleUrls: ['./coffee-preparation.component.scss']
})
export class CoffeePreparationComponent implements OnInit {

  coffeePreparationInProgress: boolean;

  constructor(private router: Router) { }

  ngOnInit() {
    this.coffeePreparationInProgress = true;

    this.setTimer();
  }


  setTimer() {
    const timer = interval(20000);
    const subscription = timer.subscribe(n => {
      console.log(`interval has been called`);
      if (this.coffeePreparationInProgress) {
        this.coffeePreparationInProgress = !this.coffeePreparationInProgress;
      } else {
        subscription.unsubscribe();
        this.router.navigate(['home']);
      }
    });
  }

}
