import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { Location } from '@angular/common';

@Component({
  selector: 'app-sign-up',
  templateUrl: './sign-up.component.html',
  styleUrls: ['./sign-up.component.scss']
})
export class SignUpComponent implements OnInit {

  constructor(private router: Router, private location: Location) { }

  ngOnInit() {
  }

  onSwipeRight () {
    this.location.back();
  }

  navigateToSignIn () {
    this.router.navigate(['sign-in']);
  }

  signUp () {
    console.log('something sign-uppy should be happening right now');
  }
}
