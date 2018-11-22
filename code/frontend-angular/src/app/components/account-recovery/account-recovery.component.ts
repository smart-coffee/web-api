import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';

@Component({
  selector: 'app-account-recovery',
  templateUrl: './account-recovery.component.html',
  styleUrls: ['./account-recovery.component.scss']
})
export class AccountRecoveryComponent implements OnInit {

  constructor(private location: Location) { }

  ngOnInit() {
  }

  onSwipeRight () {
    this.location.back();
  }

  recoverAccount () {
    console.log('something account recovery related should be happening right now...');
  }
}
