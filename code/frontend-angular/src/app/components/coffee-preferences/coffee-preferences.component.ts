import { Component, OnInit } from '@angular/core';
import { IRangeInputObject } from '../../shared/interfaces/form-input-objects';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

@Component({
  selector: 'app-coffee-preferences',
  templateUrl: './coffee-preferences.component.html',
  styleUrls: ['./coffee-preferences.component.scss']
})
export class CoffeePreferencesComponent implements OnInit {

  cupVal: number;

  headerText: string;
  waterRangeLabel: string;
  coffeeVal: number;
  waterVal: number;
  profilePickerOpen: string;

  constructor(private router: Router, private location: Location) {}

  ngOnInit() {
    this.cupVal = Number(localStorage.getItem('cupSelection'));
    this.coffeeVal = 75;
    this.waterVal = 30;
    this.profilePickerOpen = 'closed';
    this.setHeaderText();
  }

  onSwipeRight () {
    this.location.back();
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
