import { Component, OnInit } from '@angular/core';
import { Location } from '@angular/common';
import { Router } from '@angular/router';

@Component({
  selector: 'app-hot-water',
  templateUrl: './hot-water.component.html',
  styleUrls: ['./hot-water.component.scss']
})
export class HotWaterComponent implements OnInit {

  constructor(private router: Router, private location: Location) { }

  ngOnInit() {
  }

  onSwipeRight () {
    this.location.back();
  }
}
