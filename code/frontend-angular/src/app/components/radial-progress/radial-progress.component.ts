import {Component, Input, OnInit} from '@angular/core';
import {state, style} from '@angular/animations';

@Component({
  selector: 'app-radial-progress',
  templateUrl: './radial-progress.component.html',
  styleUrls: ['./radial-progress.component.scss'],
  animations: [
    state('percentage', style({
      opacity: 1,
      backgroundColor: 'green'
    })),
    state('icon', style({
      opacity: 1,
      backgroundColor: 'red'
    }))
  ]
})
export class RadialProgressComponent implements OnInit {

  @Input() type;
  @Input() width;
  //@Input() strokeWidth;
  @Input() progress;
  @Input() iconSource;

  private strokeWidth;
  private radius: number;
  private circleCenter: number;
  private circumference: number;
  private dashoffset: number;
  private colorType: string;

  constructor() { }

  ngOnInit() {
    this.strokeWidth = this.width / 10 - 1;
    // calculate circle radius, circle center coordinate, circumference and dashoffset
    this.radius = (this.width / 2) - (this.strokeWidth / 2);
    this.circleCenter = this.width / 2;
    this.circumference = 2 * Math.PI * this.radius;
    this.dashoffset = this.circumference * (1 - this.progress / 100);

    // init color type string for svg attribute
    this.colorType = this.type + 'Gradient';
  }
}
