import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

@Component({
  selector: 'app-sign-in',
  templateUrl: './sign-in.component.html',
  styleUrls: ['./sign-in.component.scss']
})
export class SignInComponent implements OnInit {

  constructor(private router: Router, private location: Location) { }

  ngOnInit() {
  }

  onSwipeRight () {
    this.location.back();
  }

  recoverPassword () {
    this.router.navigate(['account-recovery']);
  }

  signIn () {
    console.log('something sign-in related should be happening right now');
  }
}
