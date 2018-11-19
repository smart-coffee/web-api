import {Component, EventEmitter, Input, OnChanges, Output, SimpleChanges} from '@angular/core';

@Component({
  selector: 'app-button',
  templateUrl: './button.component.html',
  styleUrls: ['./button.component.scss']
})
export class ButtonComponent implements OnChanges {

  @Input() label = 'default';
  @Input() buttonType = 'default';
  @Output() action = new EventEmitter<number>();

  private numberOfClicks = 0;

  constructor() { }

  ngOnInit() {
  }

  ngOnChanges(changes: SimpleChanges) {
    console.log(changes);
  }

  handleClick(event) {
    this.numberOfClicks++;
    this.action.emit(this.numberOfClicks);
  }

}
