import { Component, OnInit } from '@angular/core';
import { animate, state, style, transition, trigger } from '@angular/animations';
import {CoffeeMachineService} from '../../services/coffee-machine.service';
import {CoffeeMachine} from '../../shared/models/coffee-machine';

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
  coffeeMachines: CoffeeMachine[];

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

  constructor(private coffeeMachineService: CoffeeMachineService) { }

  ngOnInit() {
    this.showMenu = false;

    this.coffeeMachines = [];
    this.getCoffeeMachines();

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

  getCoffeeMachines () {
    this.coffeeMachineService.getCoffeeMachines()
      .subscribe(devices => {
        devices.map(device => {
          const { uuid } = device;
          if (typeof uuid !== 'undefined') {
            this.getCoffeeMachineId(uuid);
          }
        });
      });
  }

  getCoffeeMachineId(uuid: string) {
    this.coffeeMachineService.getCoffeeMachineId(uuid)
      .subscribe(balenaDevice => {
        const { coffee_machine_id } = balenaDevice;
        if (typeof coffee_machine_id !== 'undefined') {
          this.getCoffeeMachineName(coffee_machine_id, uuid);
        } else {
          console.error(`could not retrieve balena device for uuid: ${uuid}`);
        }
      });
  }

  getCoffeeMachineName(id: number, uuid: string) {
    this.coffeeMachineService.getCoffeeMachineName(id)
      .subscribe( coffeeMachine => {
        const { name } = coffeeMachine;
        if (typeof name !== 'undefined') {
          this.coffeeMachines.push({id: id, name: name, uuid: uuid});
        } else {
          console.error(`could not retrieve coffee machine name for uuid: ${uuid} and machine id: ${id}`);
        }
      });
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
