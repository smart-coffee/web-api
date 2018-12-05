import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { animate, state, style, transition, trigger } from '@angular/animations';
import {AuthenticationService} from '../../services/authentication.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
  animations: [
    trigger('showHide', [
      state('show', style({
        opacity: 1,
        display: 'block',
        transform: 'scale(1)'
      })),
      state('hide', style({
        opacity: 0,
        display: 'none',
        transform: 'scale(0.7)'
      })),
      transition('show => hide', [
        animate('0.1s ease-in-out')
      ]),
      transition('hide => show', [
        animate('0.3s ease-in-out')
      ])
    ])
  ]
})
export class HeaderComponent implements OnInit {

  showMenu: boolean;

  constructor(private router: Router,
              private authenticationService: AuthenticationService) { }

  ngOnInit() {
    this.showMenu = false;
  }

  navigateToHome () {
    this.router.navigate(['home']);
  }

  toggleMenu () {
    this.showMenu = !this.showMenu;
  }

  signOut () {
    this.authenticationService.signOut();
    this.router.navigate(['welcome']);
  }

}
