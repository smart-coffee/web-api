import {Component, EventEmitter, Input, OnChanges, Output, SimpleChanges} from '@angular/core';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.scss']
})
export class ButtonComponent implements OnChanges {

  @Input() label: string;
  @Input() type: string;
  @Output() action = new EventEmitter<any>();

  constructor() { }

  ngOnChanges(changes: SimpleChanges) {
    console.log(changes);
  }

  handleClick(event) {
    this.action.emit(event);
  }

}
