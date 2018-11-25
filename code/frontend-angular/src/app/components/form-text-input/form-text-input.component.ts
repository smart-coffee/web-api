import { Component, EventEmitter, Input, OnInit, Output } from '@angular/core';
import { ITextInputObject } from '../../shared/interfaces/form-input-objects';

@Component({
  selector: 'app-form-text-input',
  templateUrl: './form-text-input.component.html',
  styleUrls: ['./form-text-input.component.scss']
})
export class FormTextInputComponent implements OnInit {

  @Input() label;
  @Input() name;
  @Input() type = 'text';
  @Output() typed = new EventEmitter<any>();

  inputObject: ITextInputObject;

  constructor() { }

  ngOnInit() {
    this.inputObject = {
      fieldId: '',
      value: ''
    };
  }

  onKey(event: any) {
    // save input in variable
    this.inputObject = {
      fieldId: event.target.id,
      value: event.target.value
    };

    // pass input value to parent
    this.typed.emit(this.inputObject);
  }

}
