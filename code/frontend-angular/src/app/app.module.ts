import { BrowserModule } from '@angular/platform-browser';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { NgModule } from '@angular/core';

import { AppComponent } from './app.component';
import { ServiceWorkerModule } from '@angular/service-worker';
import { environment } from '../environments/environment';
import { AppRoutingModule } from './app-routing.module';
import { SignUpComponent } from './components/sign-up/sign-up.component';
import { SignInComponent } from './components/sign-in/sign-in.component';
import { SplashComponent } from './components/splash/splash.component';
import { WelcomeComponent } from './components/welcome/welcome.component';
import { AccountRecoveryComponent } from './components/account-recovery/account-recovery.component';
import { HomeComponent } from './components/home/home.component';
import { CoffeePreferencesComponent } from './components/coffee-preferences/coffee-preferences.component';
import { AnalysisComponent } from './components/analysis/analysis.component';
import { HotWaterComponent } from './components/hot-water/hot-water.component';
import { AccountSettingsComponent } from './components/account-settings/account-settings.component';
import { ButtonComponent } from './components/button/button.component';
import { FormTextInputComponent } from './components/form-text-input/form-text-input.component';
import { ArtyHeadlineComponent } from './components/arty-headline/arty-headline.component';
import { RadialProgressComponent } from './components/radial-progress/radial-progress.component';
import { HeaderComponent } from './components/header/header.component';
import { CoffeeMachineInfoComponent } from './components/coffee-machine-info/coffee-machine-info.component';
import { APP_BASE_HREF } from '@angular/common';
import { FormRangeInputComponent } from './components/form-range-input/form-range-input.component';

@NgModule({
  declarations: [
    AppComponent,
    SignUpComponent,
    SignInComponent,
    SplashComponent,
    WelcomeComponent,
    AccountRecoveryComponent,
    HomeComponent,
    CoffeePreferencesComponent,
    AnalysisComponent,
    HotWaterComponent,
    AccountSettingsComponent,
    ButtonComponent,
    FormTextInputComponent,
    ArtyHeadlineComponent,
    RadialProgressComponent,
    HeaderComponent,
    CoffeeMachineInfoComponent,
    FormRangeInputComponent,
  ],
  imports: [
    BrowserModule,
    BrowserAnimationsModule,
    ServiceWorkerModule.register('ngsw-worker.js', { enabled: environment.production }),
    AppRoutingModule
  ],
  providers: [
    { provide: APP_BASE_HREF, useValue: '/'}
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }
