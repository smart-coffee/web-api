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

  private _error = new ServiceError();

  constructor(private http: HttpClient) { }

  getCoffeeMachines(): Observable<any> {
    return this.http.get<any>(`${environment.balenaApiUrl}/devices`)
      .pipe(
        catchError(this._error.handleError<any>(`getCoffeeMachines`))
      );
  }

  getCoffeeMachineNameById(id: number): Observable<any> {
    return this.http.get<any>(`${environment.webApiUrl}/coffee/machines/${id}`)
      .pipe(
        catchError(this._error.handleError<any>(`getCoffeeMachineName`))
      );
  }

  getCoffeeMachineStatus(uuid: string): Observable<any> {
    return this.http.get<any>(`https://${uuid}.balena-devices.com/api/device/status`)
      .pipe(
        catchError(this._error.handleError<any>(`getCoffeeMachineStatus`))
      );
  }

  getCoffeeMachineSettings(uuid: string): Observable<any> {
    return this.http.get<any>(`https://${uuid}.balena-devices.com/api/device/settings`)
      .pipe(
        catchError(this._error.handleError<any>(`getCoffeeMachineSettings`))
      );
  }
}
