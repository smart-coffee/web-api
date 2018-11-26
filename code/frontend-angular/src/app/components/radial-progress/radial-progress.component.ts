import { Component, Input, OnChanges } from '@angular/core';
import { animate, state, style, transition, trigger } from '@angular/animations';
import { interval } from 'rxjs';

@Component({
  selector: 'app-radial-progress',
  templateUrl: './radial-progress.component.html',
  styleUrls: ['./radial-progress.component.scss'],
  animations: [
    trigger('showHide', [
      state('show', style({
        opacity: 1
      })),
      state('hide', style({
        opacity: 0
      })),
      transition('show => hide', [
        animate('1s ease-in-out')
      ]),
      transition('hide => show', [
        animate('1s ease-in-out')
      ])
    ])
  ]
})
export class RadialProgressComponent implements OnChanges {

  @Input() type;
  @Input() width;
  @Input() progress;
  @Input() iconSource;

  strokeWidth;
  radius: number;
  circleCenter: number;
  circumference: number;
  dashoffset: number;
  colorType: string;
  iconWidth: number;

  percentage: boolean;

  constructor() {  }

  ngOnChanges() {
    this.percentage = true;
    // calculate stroke width according to circle size
    this.strokeWidth = this.width / 10 - 1;
    // calculate circle radius, circle center coordinate, circumference and dashoffset
    this.radius = (this.width / 2) - (this.strokeWidth / 2);
    this.circleCenter = this.width / 2;
    this.circumference = 2 * Math.PI * this.radius;
    this.dashoffset = this.circumference * (1 - this.progress / 100);
    this.iconWidth = this.width / 2 - 5;
    // init color type string for svg attribute
    this.colorType = `${this.type}Gradient`;
    // start circle animation
    this.startAnimationInterval();
  }

  startAnimationInterval() {
    // Create an Observable that will publish a value on an interval
    const secondsCounter = interval(7000);

    secondsCounter.subscribe(n => {
      this.toggleCircleLabel();
    });
  }

  toggleCircleLabel() {
    this.percentage = !this.percentage;
  }
}
