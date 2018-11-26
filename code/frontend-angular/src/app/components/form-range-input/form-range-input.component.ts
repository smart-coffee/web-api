import {Component, EventEmitter, Input, OnInit, Output} from '@angular/core';
import { IRangeInputObject } from '../../shared/interfaces/form-input-objects';

@Component({
  selector: 'app-form-range-input',
  templateUrl: './form-range-input.component.html',
  styleUrls: ['./form-range-input.component.scss']
})
export class FormRangeInputComponent implements OnInit {

  @Input() name: string;
  @Input() label: string;
  @Input() value: number;
  @Input() startIconSource: string;
  @Input() endIconSource: string;

  @Input() type: string;
  @Output() rangeChange = new EventEmitter<any>();

  inputObject: IRangeInputObject;

  localValue: number;
  minVal: number;
  maxVal: number;
  unit: string;

  constructor() { }

  ngOnInit() {
    this.localValue = this.value;

    if (this.type === 'water') {
      this.minVal = 15;
      this.maxVal = 235;
      this.unit = 'ml';
    } else {
      this.minVal = 0;
      this.maxVal = 100;
      this.unit = '%';
    }
  }

  rangeValChanged (value: any) {
    // save input in variable
    this.inputObject = {
      fieldId: this.name,
      value: value
    };

    // pass input value to parent
    this.rangeChange.emit(this.inputObject);
  }
}
