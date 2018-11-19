import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(public router: Router) { }

  canActivate(): boolean {

    if (localStorage.getItem('isLoggedIn') !== 'true') {
      this.router.navigate(['welcome']);
      return false;
    }

    return true;
  }
}
