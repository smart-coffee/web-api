import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-account-recovery',
  templateUrl: './account-recovery.component.html',
  styleUrls: ['./account-recovery.component.scss']
})
export class AccountRecoveryComponent implements OnInit {

  constructor() { }

  ngOnInit() {
  }

  recoverAccount () {
    console.log('something account recovery related should be happening right now...');
  }
}
