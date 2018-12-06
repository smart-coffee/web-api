import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { catchError } from 'rxjs/operators';
import { environment } from '../../environments/environment.prod';
import { ServiceError } from '../shared/errorhandling/service-error';

@Injectable({
  providedIn: 'root'
})
export class CoffeeMachineService {

  private error = new ServiceError();

  constructor(private http: HttpClient) { }

  getCoffeeMachines(): Observable<any> {
    return this.http.get<any>(`${environment.balenaApiUrl}/devices`)
      .pipe(
        catchError(this.error.handleError<any>(`getCoffeeMachines`))
      );
  }

  getCoffeeMachineId(uuid: string): Observable<any> {
    return this.http.get<any>(`https://${uuid}.balena-devices.com/api/device/settings`)
      .pipe(
        catchError(this.error.handleError<any>(`getCoffeeMachineId`))
      );
  }

  getCoffeeMachineName(id: number): Observable<any> {
    return this.http.get<any>(`${environment.webApiUrl}/coffee/machines/${id}`)
      .pipe(
        catchError(this.error.handleError<any>(`getCoffeeMachineName`))
      );
  }

  getCoffeeMachineStatus(uuid: string): Observable<any> {
    return this.http.get<any>(`https://${uuid}.balena-devices.com/api/device/status`)
      .pipe(
        catchError(this.error.handleError<any>(`getCoffeeMachineStatus`))
      );
  }

  getCoffeeMachineSettings(uuid: string): Observable<any> {
    return this.http.get<any>(`https://${uuid}.balena-devices.com/api/device/settings`)
      .pipe(
        catchError(this.error.handleError<any>(`getCoffeeMachineSettings`))
      );
  }
}
