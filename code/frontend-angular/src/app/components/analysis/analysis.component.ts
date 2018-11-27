import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-analysis',
  templateUrl: './analysis.component.html',
  styleUrls: ['./analysis.component.scss']
})
export class AnalysisComponent implements OnInit {

  min = 0;
  max = 100;
  twoWayRange = [10, 30];

  constructor() { }

  ngOnInit() {
  }

  changed() {
    this.twoWayRange = [...this.twoWayRange];
  }
}
