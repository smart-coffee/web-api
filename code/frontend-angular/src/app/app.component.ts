import { Component } from '@angular/core';
import { SwUpdate } from '@angular/service-worker';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  title = 'smart-coffee-angular';

  constructor (update: SwUpdate) {
    update.available.subscribe(event => {
      update.activateUpdate().then(() => document.location.reload());
    });
  }
}
