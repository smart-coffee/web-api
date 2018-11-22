import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-arty-headline',
  templateUrl: './arty-headline.component.html',
  styleUrls: ['./arty-headline.component.scss']
})
export class ArtyHeadlineComponent implements OnInit {

  @Input() text = 'default';
  @Input() artSource: string;

  constructor() { }

  ngOnInit() {
  }

}
