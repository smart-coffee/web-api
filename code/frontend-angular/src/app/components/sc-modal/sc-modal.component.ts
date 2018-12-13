import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-error-modal',
  templateUrl: './sc-modal.component.html',
  styleUrls: ['./sc-modal.component.scss']
})
export class ScModalComponent implements OnInit {

  @Input() type: string;
  @Input() message: string;

  constructor() { }

  ngOnInit() {
  }

}
