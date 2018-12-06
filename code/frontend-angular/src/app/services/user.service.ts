import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment.prod';
import { catchError } from 'rxjs/operators';
import { ServiceError } from '../shared/errorhandling/service-error';

@Injectable({
  providedIn: 'root'
})
export class UserService {

  private error = new ServiceError();

  constructor(private http: HttpClient) { }

  getCoffeeProfiles(): Observable<any> {
    return this.http.get<any>(`${environment.webApiUrl}/users/current/profiles`)
      .pipe(
        catchError(this.error.handleError<any>(`getCoffeeProfiles`))
      );
  }


}
