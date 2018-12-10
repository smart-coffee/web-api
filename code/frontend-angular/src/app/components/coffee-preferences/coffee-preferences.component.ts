import { Component, OnInit } from '@angular/core';
import {IRangeInputObject, ITextInputObject} from '../../shared/interfaces/form-input-objects';
import { CoffeeProfile } from '../../shared/models/coffee-profile';
import { UserService } from '../../services/user.service';
import {animate, state, style, transition, trigger} from '@angular/animations';

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

  showEditProfileModal: boolean;
  editProfileModalNewProfile: boolean;
  newCoffeeProfileName: string;

  headerText: string;
  waterRangeLabel: string;
  coffeeVal: number;
  waterVal: number;
  profilePickerOpen: string;

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.cupVal = Number(localStorage.getItem('cupSelection'));
    this.defaultProfile = {id: 0, name: 'Italienischer Espresso', coffeeVal: 75, waterVal: 30};
    this.coffeeVal = this.defaultProfile.coffeeVal;
    this.waterVal = this.defaultProfile.waterVal;
    this.profilePickerOpen = 'closed';
    this.showEditProfileModal = false;
    this.editProfileModalNewProfile = false;
    this.setHeaderText();
    this.getCoffeeProfiles();
    this.selectedProfile = this.defaultProfile;
  }

  resetCoffeeProfiles() {
    this.coffeeProfiles = [
      {id: 0, name: 'Italienischer Espresso', coffeeVal: 75, waterVal: 30}
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
    console.log(`a coffee job is being sent`);
  }

  saveNewProfile() {
    console.log(`the new profile "${this.newCoffeeProfileName}" with the coffee 
    value ${this.coffeeVal} and water value ${this.waterVal} is being saved`);
    this.resetEditProfileModalState();
  }

  toggleProfilePicker() {
    if (this.profilePickerOpen === 'closed') {
      this.profilePickerOpen = 'open';
    } else {
      this.profilePickerOpen = 'closed';
    }
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
            waterVal: Math.round(water_in_percent * 220 / 100)
          };
          this.coffeeProfiles = [...this.coffeeProfiles, tmp];
        });
      });
  }

}
