import { Component, OnInit } from '@angular/core';
import { IRangeInputObject } from '../../shared/interfaces/form-input-objects';
import {CoffeeProfile} from '../../shared/models/coffee-profile';

@Component({
  selector: 'app-coffee-preferences',
  templateUrl: './coffee-preferences.component.html',
  styleUrls: ['./coffee-preferences.component.scss']
})
export class CoffeePreferencesComponent implements OnInit {

  coffeeProfiles: CoffeeProfile[];
  selectedProfile: CoffeeProfile;
  defaultProfile: CoffeeProfile;

  cupVal: number;

  headerText: string;
  waterRangeLabel: string;
  coffeeVal: number;
  waterVal: number;
  profilePickerOpen: string;

  constructor() {}

  ngOnInit() {
    this.cupVal = Number(localStorage.getItem('cupSelection'));
    this.defaultProfile = {id: 0, name: 'Italienischer Espresso', coffeeVal: 75, waterVal: 30};
    this.coffeeVal = this.defaultProfile.coffeeVal;
    this.waterVal = this.defaultProfile.waterVal;
    this.profilePickerOpen = 'closed';
    this.setHeaderText();

    this.coffeeProfiles = [
      {id: 0, name: 'Italienischer Espresso', coffeeVal: 75, waterVal: 30},
      {id: 1, name: 'Stark', coffeeVal: 100, waterVal: 30},
      {id: 2, name: 'Fast schon Wasser', coffeeVal: 10, waterVal: 235}
    ];

    this.selectedProfile = this.defaultProfile;
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

  toggleProfilePicker() {
    if (this.profilePickerOpen === 'closed') {
      this.profilePickerOpen = 'open';
    } else {
      this.profilePickerOpen = 'closed';
    }
  }

}
