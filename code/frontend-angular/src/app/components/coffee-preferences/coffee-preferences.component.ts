import { Component, OnInit } from '@angular/core';
import { IRangeInputObject } from '../../shared/interfaces/form-input-objects';
import { CoffeeProfile } from '../../shared/models/coffee-profile';
import { UserService } from '../../services/user.service';

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

  constructor(private userService: UserService) {}

  ngOnInit() {
    this.cupVal = Number(localStorage.getItem('cupSelection'));
    this.defaultProfile = {id: 0, name: 'Italienischer Espresso', coffeeVal: 75, waterVal: 30};
    this.coffeeVal = this.defaultProfile.coffeeVal;
    this.waterVal = this.defaultProfile.waterVal;
    this.profilePickerOpen = 'closed';
    this.setHeaderText();

    this.coffeeProfiles = [
      {id: 0, name: 'Italienischer Espresso', coffeeVal: 75, waterVal: 30}
    ];
    this.getCoffeeProfiles();
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

  getCoffeeProfiles() {
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
