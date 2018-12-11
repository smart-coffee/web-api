import { Component, OnInit } from '@angular/core';
import { ITextInputObject } from '../../shared/interfaces/form-input-objects';
import { Router } from '@angular/router';
import { Location } from '@angular/common';
import { UserService } from '../../services/user.service';

@Component({
  selector: 'app-account-settings',
  templateUrl: './account-settings.component.html',
  styleUrls: ['./account-settings.component.scss']
})
export class AccountSettingsComponent implements OnInit {

  username: string;
  oldPassword: string;
  newPassword: string;
  newPasswordConfirm: string;
  email: string;

  constructor(private router: Router,
              private location: Location,
              private userService: UserService) { }

  ngOnInit() {
    this.username = '';
    this.oldPassword = '';
    this.newPassword = '';
    this.newPasswordConfirm = '';
    this.email = '';
  }

  onSwipeRight () {
    this.goBack();
  }

  goBack() {
    this.location.back();
  }

  onTyped (inputInfo: ITextInputObject ) {
    switch (inputInfo.fieldId) {
      case 'username': this.username = inputInfo.value; break;
      case 'oldPassword': this.oldPassword = inputInfo.value; break;
      case 'newPassword': this.newPassword = inputInfo.value; break;
      case 'newPasswordConfirm': this.newPasswordConfirm = inputInfo.value; break;
      case 'email': this.email = inputInfo.value; break;
      default: console.error('something broke in the sign in input distinction');
    }
  }

  editUser() {
    if (this.newPassword === this.newPasswordConfirm) {
      const tmpUser = {
        name: this.username,
        old_password: this.oldPassword,
        new_password: this.newPassword,
        email: this.email
      };
      this.userService.editUserDetails(tmpUser)
        .subscribe(user => {
          console.log(user);
        });
    }
  }

}
