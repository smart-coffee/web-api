import { Component, OnInit } from '@angular/core';
import { animate, state, style, transition, trigger } from '@angular/animations';

@Component({
  selector: 'app-coffee-machine-info',
  templateUrl: './coffee-machine-info.component.html',
  styleUrls: ['./coffee-machine-info.component.scss'],
  animations: [
    trigger('showHide', [
      state('show', style({
        opacity: 1,
        display: 'block',
        transform: 'translateX(0)'
      })),
      state('hide', style({
        opacity: 0,
        display: 'none',
        transform: 'translateY(-50px)'
      })),
      transition('show => hide', [
        animate('0.1s ease-in-out')
      ]),
      transition('hide => show', [
        animate('0.3s ease-in-out')
      ])
    ])
  ]
})
export class CoffeeMachineInfoComponent implements OnInit {

  showMenu: boolean;

  coffeeMachines: Object = [
    { name: 'Winston' },
    { name: 'Reinhart' },
    { name: 'Moira' }
  ];

  coffeeMachineDetails = {
    name: '',
    coffeeLevel: 0,
    waterLevel: 0,
    trashLevel: 0
  };

  coffeeMachineDetailsList: Object = [
    {name: 'Winston', coffeeLevel: 90, waterLevel: 73, trashLevel: 20},
    {name: 'Reinhart', coffeeLevel: 50, waterLevel: 40, trashLevel: 60},
    {name: 'Moira', coffeeLevel: 22, waterLevel: 50, trashLevel: 85},
  ];

  constructor() { }

  ngOnInit() {
    this.showMenu = false;

    this.coffeeMachineDetails = {
      name: 'Winston',
      coffeeLevel: 90,
      waterLevel: 73,
      trashLevel: 20
    };
  }

  toggleMenu () {
    this.showMenu = !this.showMenu;
  }

  pickMachine (machineName: string) {
    this.coffeeMachineDetails = this.search(machineName, this.coffeeMachineDetailsList);
  }

  search (nameKey: string, array: any) {
    for (let i = 0; i < array.length; i++) {
      if (array[i].name === nameKey) {
        return array[i];
      }
    }
  }

}
