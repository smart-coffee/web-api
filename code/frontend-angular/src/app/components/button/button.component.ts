import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.scss']
})
export class ButtonComponent implements OnInit {

  @Input() label: string;
  @Input() type: string;
  @Input() enabled: boolean;
  @Output() action = new EventEmitter<any>();

  constructor() { }

  ngOnInit() { }

  handleClick(event) {
    if (this.enabled) {
      this.action.emit(event);
    }
  }

}
