import {ChangeDetectorRef, Component, OnInit} from '@angular/core';
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

  detailsLoading: boolean;
  showMenu: boolean;
  coffeeMachines: CoffeeMachine[];
  machineDetailsInitialized: boolean;

  coffeeMachineDetails = {
    name: '',
    coffeeLevel: 0,
    waterLevel: 0,
    trashLevel: 0
  };

  constructor(private coffeeMachineService: CoffeeMachineService,
              private cdr: ChangeDetectorRef) { }

  ngOnInit() {
    this.detailsLoading = true;
    this.showMenu = false;
    this.machineDetailsInitialized = false;
    this.coffeeMachines = [];
    this.getCoffeeMachines();
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
        }
      );
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
          this.coffeeMachines = [...this.coffeeMachines, {id: id, name: name, uuid: uuid}];
          if (!this.machineDetailsInitialized) {
            this.initCoffeeMachineDetails({id: id, name: name, uuid: uuid});
            localStorage.setItem('currentMachine', JSON.stringify({id: id, name: name, uuid: uuid}));
            this.machineDetailsInitialized = true;
          }
        } else {
          console.error(`could not retrieve coffee machine name for uuid: ${uuid} and machine id: ${id}`);
        }
      });
  }

  initCoffeeMachineDetails(cm: CoffeeMachine) {
    this.detailsLoading = true;
    const { name, uuid } = cm;
    this.coffeeMachineService.getCoffeeMachineStatus(uuid)
      .subscribe( coffeeMachine => {
        const { water_tank_fill_level_in_percent: waterLevel,
          coffee_bean_container_fill_level_in_percent: coffeeLevel,
          coffee_grounds_container_fill_level_in_percent: trashLevel } = coffeeMachine;

        if (typeof waterLevel !== 'undefined' && typeof coffeeLevel !== 'undefined' && typeof trashLevel !== 'undefined') {
          this.coffeeMachineDetails = {
            name: name,
            coffeeLevel: coffeeLevel,
            waterLevel: waterLevel,
            trashLevel: trashLevel
          };
          this.detailsLoading = false;
          this.cdr.detectChanges();
        }
      });
  }

}
