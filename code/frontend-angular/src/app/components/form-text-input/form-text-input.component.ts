import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'app-form-text-input',
  templateUrl: './form-text-input.component.html',
  styleUrls: ['./form-text-input.component.scss']
})
export class FormTextInputComponent implements OnInit {

  @Input() label;
  @Input() name;
  @Input() type = 'text';

  constructor() { }

  ngOnInit() {
  }

}
