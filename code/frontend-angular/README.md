# Frontend Angular

This project was generated with [Angular CLI](https://github.com/angular/angular-cli) version 7.0.6.

## Prerequisites

* Node.js LTS (v10.13.0)
* npm latest (v6.4.1)
* http-server npm module (`npm i -g http-server`)

## Development server

Keep the modules up to date with `npm install` before building the application

Run `ng serve --open` for a dev server. Navigate to `http://localhost:4200/`. The app will automatically reload if you change any of the source files.

This is also a Progressive Web App (PWA) with dedicated [service workers](https://angular.io/guide/service-worker-intro). Service workers do not function in an angular development environment. To test the PWA functionality execute the following steps:

1. Build a production  build of the app with `ng build --prod`
2. Start a http server with the http-server npm package `http-server -p 8080 -c-1 dist/frontend-angular`
3. Navigate to `localhost:8080`

*common mistakes*: old cache -> clear before throwing your laptop out of a window because something is not working as intended


## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|guard|interface|enum|module`.

## Build

Run `ng build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `--prod` flag for a production build.

## Running unit tests (*this feature is turned off*)

Run `ng test` to execute the unit tests via [Karma](https://karma-runner.github.io).

## Running end-to-end tests

Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).

## Further help

To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
