import { AfterViewInit, Component } from '@angular/core';
import { SwUpdate } from '@angular/service-worker';
import { Router, NavigationStart, NavigationCancel, NavigationEnd } from '@angular/router';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements AfterViewInit {
  title = 'smart-coffee-angular';

  loading: boolean;

  constructor (update: SwUpdate, private router: Router) {
    update.available.subscribe(event => {
      update.activateUpdate().then(() => document.location.reload());
    });

    this.loading = true;
  }

  ngAfterViewInit() {
    this.router.events
      .subscribe((event) => {
        if (event instanceof NavigationStart) {
          this.loading = true;
        } else if (event instanceof NavigationEnd || event instanceof NavigationCancel) {
          this.loading = false;
        }
      });
  }
}
