import { Injectable } from '@angular/core';
import { CanActivate, Router } from '@angular/router';

@Injectable({
  providedIn: 'root'
})
export class AuthGuard implements CanActivate {

  constructor(public router: Router) { }

  canActivate(): boolean {

    // TODO: don't forget changing this shit
    if (localStorage.getItem('isLoggedIn') !== 'true') {
      this.router.navigate(['welcome']);
      return false;
    }

    return true;
  }
}
