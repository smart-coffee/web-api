import { Component, OnInit } from '@angular/core';
import {Router} from '@angular/router';
import {CoffeeMachineService} from '../../services/coffee-machine.service';
import {CoffeeMachine} from '../../shared/models/coffee-machine';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {

  coffeeMachines: CoffeeMachine[];

  constructor(private router: Router) { }

  ngOnInit() { }



  navigateToRoute (routeName: string) {
    this.router.navigate([routeName]);
  }

}
