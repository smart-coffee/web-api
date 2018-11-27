import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { WelcomeComponent } from './components/welcome/welcome.component';
import { AccountRecoveryComponent } from './components/account-recovery/account-recovery.component';
import { CoffeePreferencesComponent } from './components/coffee-preferences/coffee-preferences.component';
import { HomeComponent } from './components/home/home.component';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import { SignInComponent } from './components/sign-in/sign-in.component';
import { AuthGuard } from './auth-guard.service';
import { AnalysisComponent } from './components/analysis/analysis.component';

/**
 * App routing module contains all routes for the application
 * All routes are sorted alphabetically for ease of use
 */

const routes: Routes = [
  { path: '', canActivate: [AuthGuard], pathMatch: 'full', redirectTo: 'home' },
  { path: 'account-recovery', component: AccountRecoveryComponent },
  { path: 'analysis', component: AnalysisComponent},
  { path: 'coffee-preferences', component: CoffeePreferencesComponent },
  { path: 'home', canActivate: [AuthGuard], component: HomeComponent },
  { path: 'sign-up', component: SignUpComponent },
  { path: 'sign-in', component: SignInComponent  },
  { path: 'welcome', component: WelcomeComponent }
];

@NgModule({
  imports: [ RouterModule.forRoot(routes) ],
  exports: [ RouterModule ]
})
export class AppRoutingModule { }
