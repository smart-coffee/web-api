import { Component, OnInit } from '@angular/core';
import { animate, state, style, transition, trigger } from '@angular/animations';
import {Router} from '@angular/router';

@Component({
  selector: 'app-coffee-machine-info',
  templateUrl: './coffee-machine-info.component.html',
  styleUrls: ['./coffee-machine-info.component.scss'],
  animations: [
    trigger('showHide', [
      state('show', style({
        opacity: 1,
        display: 'block',
        transform: 'translateX(0)'
      })),
      state('hide', style({
        opacity: 0,
        display: 'none',
        transform: 'translateY(-50px)'
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
export class CoffeeMachineInfoComponent implements OnInit {

  showMenu: boolean;

  constructor() { }

  ngOnInit() {
    this.showMenu = false;
  }

  toggleMenu () {
    this.showMenu = !this.showMenu;
  }

}
