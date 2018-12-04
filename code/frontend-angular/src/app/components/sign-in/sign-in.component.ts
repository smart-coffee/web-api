import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import { ITextInputObject } from '../../shared/interfaces/form-input-objects';
import { first } from 'rxjs/operators';
import { AuthenticationService } from '../../services/authentication.service';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.scss']
})
export class SignInComponent implements OnInit {

  username: string;
  password: string;
  loading: boolean;
  error: string;

  constructor(private router: Router,
              private location: Location,
              private authenticationService: AuthenticationService
  ) { }

  ngOnInit() {
    this.username = '';
    this.password = '';
    this.loading = false;
    this.error = '';
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
    this.loading = true;
    this.authenticationService.login(this.username, this.password)
      .pipe(first())
      .subscribe(
        data => {
          this.router.navigate(['home']);
        },
        error => {
          this.error = error;
          this.loading = false;
        }
      );
  }
}
