import { Component, OnInit } from '@angular/core';
import { IRangeInputObject, ITextInputObject } from '../../shared/interfaces/form-input-objects';
import { CoffeeProfile } from '../../shared/models/coffee-profile';
import { UserService } from '../../services/user.service';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { CoffeeMachineService } from '../../services/coffee-machine.service';
import { Router } from '@angular/router';
import { interval } from 'rxjs';

@Component({
  selector: 'app-coffee-preferences',
  templateUrl: './coffee-preferences.component.html',
  styleUrls: ['./coffee-preferences.component.scss'],
  animations: [
    trigger('showHide', [
      state('show', style({
        opacity: 1,
        display: 'block',
        transform: 'scale(1)'
      })),
      state('hide', style({
        opacity: 0,
        display: 'none',
        transform: 'scale(0.7)'
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
export class CoffeePreferencesComponent implements OnInit {

  coffeeProfiles: CoffeeProfile[];
  selectedProfile: CoffeeProfile;
  defaultProfile: CoffeeProfile;

  cupVal: number;

  showNotificationModal: boolean;
  modalMessages: string[];
  modalType: string;
  showEditProfileModal: boolean;
  editProfileModalNewProfile: boolean;
  newCoffeeProfileName: string;
  saveProfileSent: boolean;
  coffeeJobSendInProgress: boolean;

  startButtonText: string;
  startButtonTextX: number;
  headerText: string;
  waterRangeLabel: string;
  coffeeVal: number;
  waterVal: number;
  profilePickerOpen: string;

  constructor(private userService: UserService,
              private coffeeMachineService: CoffeeMachineService,
              private router: Router) {}

  ngOnInit() {
    this.cupVal = Number(localStorage.getItem('cupSelection'));
    this.defaultProfile = {id: 0, name: 'Italienischer Espresso', coffeeVal: 75, waterVal: 30};
    this.coffeeVal = this.defaultProfile.coffeeVal;
    this.waterVal = this.defaultProfile.waterVal;
    this.profilePickerOpen = 'closed';
    this.startButtonText = 'Start';
    this.startButtonTextX = 12.8275; // filthy, i know
    this.showEditProfileModal = false;
    this.editProfileModalNewProfile = false;
    this.saveProfileSent = true;
    this.coffeeJobSendInProgress = false;
    this.showNotificationModal = false;
    this.modalMessages = [];
    this.modalType = 'info';
    this.setHeaderText();
    this.getCoffeeProfiles();
    this.selectedProfile = this.defaultProfile;
  }

  resetCoffeeProfiles() {
    this.coffeeProfiles = [
      this.defaultProfile
    ];
  }

  selectProfile(profile: CoffeeProfile) {
    this.selectedProfile = profile;
    this.waterVal = profile.waterVal;
    this.coffeeVal = profile.coffeeVal;
  }

  onRangeChange (inputObject: IRangeInputObject) {
    switch (inputObject.fieldId) {
      case 'coffee-preferences': this.coffeeVal = inputObject.value; break;
      case 'water-preferences': this.waterVal = inputObject.value; break;
      default: console.error('something broke in the coffee preferences input distinction');
    }
  }

  setHeaderText() {
    if (this.cupVal === 1) {
      this.headerText = 'Eine Tasse';
      this.waterRangeLabel = '';
    } else {
      this.headerText = 'Zwei Tassen';
      this.waterRangeLabel = '(pro Tasse)';
    }
  }

  setEditProfileModalState(modalState: string) {

    if (modalState === 'newProfile') {
      this.showEditProfileModal = true;
      this.editProfileModalNewProfile = true;
    } else if (modalState === 'cancelNew') {
      this.resetEditProfileModalState();
    } else if (modalState === 'continueWithout') {
      this.sendCoffeeJob();
      this.resetEditProfileModalState();
    } else if (modalState === 'profileChanged') {
      this.showEditProfileModal = true;
    } else {
      this.resetEditProfileModalState();
    }
  }

  resetEditProfileModalState() {
    this.showEditProfileModal = false;
    this.editProfileModalNewProfile = false;
  }

  onTyped (inputInfo: ITextInputObject ) {
    switch (inputInfo.fieldId) {
      case 'profile-name': this.newCoffeeProfileName = inputInfo.value; break;
      default: console.error('something broke in the sign in input distinction');
    }
  }

  attemptSendingCoffeeJob() {
    if (Number(this.coffeeVal) !== Number(this.selectedProfile.coffeeVal)
      || Number(this.waterVal) !== Number(this.selectedProfile.waterVal)) {
      this.setEditProfileModalState('profileChanged');
    } else {
      this.sendCoffeeJob();
    }
  }

  sendCoffeeJob() {
    if (!this.coffeeJobSendInProgress) {
      this.coffeeJobSendInProgress = true;
      const currentMachine = JSON.parse(localStorage.getItem('currentMachine'));
      const jobDetails = {
        coffee_strength_in_percent: Number(this.coffeeVal),
        water_in_percent: this.waterValToPercent(Number(this.waterVal)),
        doses: Number(this.cupVal)
      };

      const timer = interval(800);
      const subscription = timer.subscribe(n => {
        if (this.startButtonText === '...' || this.startButtonText === 'Start') {
          this.startButtonText = '';
          this.startButtonTextX = 27;
        } else {
          this.startButtonText = this.startButtonText + '.';
        }
      });

      this.coffeeMachineService.postNewCoffeeJob(currentMachine.uuid, jobDetails)
        .subscribe( jobConfirmation => {
          subscription.unsubscribe();
          this.coffeeJobSendInProgress = false;
          if (jobConfirmation) {
            this.router.navigate(['coffee-preparation']);
          } else {
            this.startButtonText = 'Start';
            this.startButtonTextX = 12.8275;
            console.error(`something went wrong processing the new coffee job`);
          }
        });
    }
  }

  saveNewProfile() {
    if (typeof this.newCoffeeProfileName !== 'undefined' && this.newCoffeeProfileName) {
      this.saveProfileSent = false;
      const tmpProfile = {
        coffee_strength_in_percent: Number(this.coffeeVal),
        name: this.newCoffeeProfileName,
        water_in_percent: this.waterValToPercent(Number(this.waterVal)),
      };
      this.userService.postNewCoffeeProfile(tmpProfile)
        .subscribe(coffeeProfile => {
          this.saveProfileSent = true;
          this.getCoffeeProfiles();
          this.modalMessages = ['Dein neues Kaffeeprofil wurde erfolgreich gespeichert'];
          this.modalType = 'info';
          this.showNotificationModal = true;
          this.resetEditProfileModalState();
          setTimeout(() => {
            this.showNotificationModal = false;
          }, 3000);
        }, error => {
          this.showNotificationModal = true;
          this.modalType = 'error';
          this.modalMessages = [error];
        });
    }
  }

  toggleProfilePicker() {
    if (this.profilePickerOpen === 'closed') {
      this.profilePickerOpen = 'open';
    } else {
      this.profilePickerOpen = 'closed';
    }
  }

  waterValToMl(waterValInPercent: number): number {
    return Math.round((waterValInPercent / 1000 * 220 / 100) + 15);
  }

  waterValToPercent(waterValInMl: number): number {
    return Math.round((((waterValInMl - 15) * 100) / 220) * 1000);
  }

  getCoffeeProfiles() {
    this.resetCoffeeProfiles();
    this.userService.getCoffeeProfiles()
      .subscribe(profiles => {
        profiles.map(profile => {
          const { coffee_strength_in_percent, water_in_percent, name, id } = profile;
          const tmp = {
            id: id,
            name: name,
            coffeeVal: coffee_strength_in_percent,
            waterVal: this.waterValToMl(water_in_percent)
          };
          this.coffeeProfiles = [...this.coffeeProfiles, tmp];
        });
      }, error => {
        this.showNotificationModal = true;
        this.modalType = 'error';
        this.modalMessages = [error];
      });
  }

}
