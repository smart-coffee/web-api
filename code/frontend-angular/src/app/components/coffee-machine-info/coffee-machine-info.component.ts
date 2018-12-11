import {ChangeDetectorRef, Component, EventEmitter, OnInit, Output} from '@angular/core';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { CoffeeMachineService } from '../../services/coffee-machine.service';
import { CoffeeMachine } from '../../shared/models/coffee-machine';
import { CoffeeMachineDetails } from '../../shared/models/coffee-machine-details';
import { CoffeeService } from '../../services/coffee.service';

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
  showMachineDropdown: boolean;
  showCoffeeDetails: boolean;
  coffeeMachines: CoffeeMachine[];
  machineDetailsInitialized: boolean;
  @Output() detailsLoaded = new EventEmitter<boolean>();

  coffeeMachineDetails: CoffeeMachineDetails;

  constructor(private coffeeMachineService: CoffeeMachineService,
              private coffeeService: CoffeeService,
              private cdr: ChangeDetectorRef) { }

  ngOnInit() {
    this.detailsLoading = true;
    this.showMachineDropdown = false;
    this.showCoffeeDetails = false;
    this.machineDetailsInitialized = false;
    this.coffeeMachines = [];
    this.detailsLoaded.emit(false);
    this.resetCoffeeMachineDetails();
    this.getCoffeeMachines();
  }

  resetCoffeeMachineDetails() {
    this.coffeeMachineDetails = {
      name: '',
      coffeeLevel: 0,
      waterLevel: 0,
      trashLevel: 0,
      pricePerCoffeeInCents: 0,
      coffeeBrand: '',
      coffeeType: ''
    };
  }

  toggleMachinePicker () {
    this.showMachineDropdown = !this.showMachineDropdown;
  }

  toggleCoffeeDetails () {
    this.showCoffeeDetails = !this.showCoffeeDetails;
  }

  getCoffeeMachines () {
    this.coffeeMachineService.getCoffeeMachines()
      .subscribe(devices => {
          devices.map(device => {
            const { uuid } = device;
            if (typeof uuid !== 'undefined') {
            this.getCoffeeMachineSettings(uuid);
            }
          });
        }
      );
  }

  getCoffeeMachineSettings(uuid: string) {
    this.coffeeMachineService.getCoffeeMachineSettings(uuid)
      .subscribe(balenaDevice => {
        const { coffee_machine_id: machineId } = balenaDevice;
        if (typeof machineId !== 'undefined') {
          this.getCoffeeMachineDetails(machineId, uuid);
        } else {
          console.error(`could not retrieve balena device for undefined uuid`);
        }
      });
  }

  getCoffeeMachineDetails(machineId: number, uuid: string) {
    this.coffeeMachineService.getCoffeeMachineNameById(machineId)
      .subscribe( coffeeMachine => {
        const { name } = coffeeMachine;
        if (typeof name !== 'undefined') {
          const tmpMachine = {id: machineId, name: name, uuid: uuid};
          this.coffeeMachines = [...this.coffeeMachines, tmpMachine];
          this.initCoffeeMachineDetails(tmpMachine);
          if (!this.machineDetailsInitialized) {
            this.initCoffeeMachineDetails(tmpMachine);
            this.machineDetailsInitialized = true;
          }
        }
      });
  }

  initCoffeeMachineDetails(cm: CoffeeMachine) {
    this.detailsLoading = true;
    this.detailsLoaded.emit(false);

    const { name, uuid } = cm;
    localStorage.setItem('currentMachine', JSON.stringify(cm));

    this.coffeeMachineService.getCoffeeMachineStatus(uuid)
      .subscribe( coffeeMachineStatus => {
        const { water_tank_fill_level_in_percent: waterLevel,
          coffee_bean_container_fill_level_in_percent: coffeeLevel,
          coffee_grounds_container_fill_level_in_percent: trashLevel } = coffeeMachineStatus;

        if (typeof waterLevel !== 'undefined' && typeof coffeeLevel !== 'undefined' && typeof trashLevel !== 'undefined') {
          this.coffeeMachineDetails.name = name;
          this.coffeeMachineDetails.coffeeLevel = coffeeLevel;
          this.coffeeMachineDetails.waterLevel = waterLevel;
          this.coffeeMachineDetails.trashLevel = trashLevel;

          // get the product id -> product name -> product type
          this.coffeeMachineService.getCoffeeMachineSettings(uuid)
            .subscribe( coffeeMachineSettings => {
              const { coffee_product_id, price } = coffeeMachineSettings;
              this.coffeeMachineDetails.pricePerCoffeeInCents = price;
              this.getCoffeeProductById(coffee_product_id);
            });
        }
      });
  }

  getCoffeeProductById(id: number) {
    this.coffeeService.getCoffeeProductById(id)
      .subscribe( coffeeProduct => {
        const { name, coffee_brand_id } = coffeeProduct;
        if (typeof name !== 'undefined') {
          this.coffeeMachineDetails.coffeeBrand = name;
        }

        if (typeof coffee_brand_id !== 'undefined') {
          this.getCoffeeTypeById(coffee_brand_id);
        }
      });
  }

  getCoffeeTypeById(id: number) {
    this.coffeeService.getCoffeeTypeById(id)
      .subscribe( coffeeType => {
        const { name } = coffeeType;
        if (typeof name !== 'undefined') {
          this.coffeeMachineDetails.coffeeType = name;
          this.detailsLoading = false;
          this.cdr.detectChanges();
          this.detailsLoaded.emit(true);
        }
      });
  }

}
