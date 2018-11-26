import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import { ITextInputObject } from '../../shared/interfaces/form-input-objects';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.scss']
})
export class SignInComponent implements OnInit {

  username: string;
  password: string;

  constructor(private router: Router, private location: Location) { }

  ngOnInit() {
    this.username = '';
    this.password = '';
  }

  onSwipeRight () {
    this.location.back();
  }

  recoverPassword () {
    this.router.navigate(['account-recovery']);
  }

  onTyped (inputInfo: ITextInputObject ) {
    switch (inputInfo.fieldId) {
      case 'username': this.username = inputInfo.value; break;
      case 'password': this.password = inputInfo.value; break;
      default: console.error('something broke in the sign in input distinction');
    }
  }

  signIn () {
    if (this.username === 'admin' && this.password === 'admin') {
      localStorage.setItem('isLoggedIn', 'true');
      console.log('something sign-in related should be happening right now -' +
        ' it is not though ... you just hacked your way in');
      console.log('you sneaky little hacker ヽ༼ ಠ益ಠ ༽ﾉ');
      this.router.navigate(['home']);
    } else {
      console.log('WOW .... nice try hacking this super secure application ... try again with a different password');
    }
  }
}
