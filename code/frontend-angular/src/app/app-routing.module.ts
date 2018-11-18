import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { SplashComponent } from './components/splash/splash.component';
import { WelcomeComponent } from './components/welcome/welcome.component';
import { AccountRecoveryComponent } from './components/account-recovery/account-recovery.component';
import { CoffeePreferencesComponent } from './components/coffee-preferences/coffee-preferences.component';
import { HomeComponent } from './components/home/home.component';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import { SignInComponent } from './components/sign-in/sign-in.component';

/**
 * App routing module contains all routes for the application
 * All routes EXCEPT 'splash' are sorted alphabetically for ease of use
 */

const routes: Routes = [
  { path: '', component: SplashComponent },
  { path: 'account-recovery', component: AccountRecoveryComponent },
  { path: 'coffee-preferences', component: CoffeePreferencesComponent },
  { path: 'home', component: HomeComponent },
  { path: 'sign-up', component: SignUpComponent },
  { path: 'sign-in', component: SignInComponent  },
  { path: 'welcome', component: WelcomeComponent }
];

@NgModule({
  exports: [ RouterModule ]
})
export class AppRoutingModule { }
