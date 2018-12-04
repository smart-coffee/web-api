import {Component, EventEmitter, Input, OnInit, Output, SimpleChanges} from '@angular/core';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.scss']
})
export class ButtonComponent implements OnInit {

  @Input() label: string;
  @Input() type: string;
  @Output() action = new EventEmitter<any>();

  constructor() { }

  ngOnInit() { }

  handleClick(event) {
    this.action.emit(event);
  }

}
