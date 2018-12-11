import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import {UserService} from '../../services/user.service';
import {ITextInputObject} from '../../shared/interfaces/form-input-objects';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss']
})
export class SignUpComponent implements OnInit {

  // TODO: form validation
  username: string;
  password: string;
  passwordConfirm: string;
  email: string;

  constructor(private router: Router,
              private location: Location,
              private userService: UserService) { }

  ngOnInit() {
    this.username = '';
    this.password = '';
    this.passwordConfirm = '';
    this.email = '';
  }

  onSwipeRight () {
    this.location.back();
  }

  navigateToSignIn () {
    this.router.navigate(['sign-in']);
  }

  onTyped (inputInfo: ITextInputObject ) {
    switch (inputInfo.fieldId) {
      case 'username': this.username = inputInfo.value; break;
      case 'password': this.password = inputInfo.value; break;
      case 'passwordConfirm': this.passwordConfirm = inputInfo.value; break;
      case 'email': this.email = inputInfo.value; break;
      default: console.error('something broke in the sign in input distinction');
    }
  }

  signUp () {
    if (this.password === this.passwordConfirm) {
      const newUser = {
        name: this.username,
        password: this.password,
        email: this.email
      };
      this.userService.postNewUser(newUser)
        .subscribe( user => {
          console.log(user);
        });
    }
    console.log('something sign-uppy should be happening right now');
  }
}
