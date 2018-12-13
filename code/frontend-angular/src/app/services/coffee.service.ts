import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import {Observable, Subject} from 'rxjs';
import { environment } from '../../environments/environment.prod';
import { catchError } from 'rxjs/operators';
import { ServiceError } from '../shared/errorhandling/service-error';
import {Cacheable} from 'ngx-cacheable';

const cacheBuster = new Subject<void>();

@Injectable({
  providedIn: 'root'
})
export class CoffeeService {

  private _error = new ServiceError();

  constructor(private http: HttpClient) { }

  @Cacheable({
    cacheBusterObserver: cacheBuster,
    maxAge: 900000
  })
  getCoffeeProductById(id: number): Observable<any> {
    return this.http.get<any>(`${environment.webApiUrl}/coffee/products/${id}`)
      .pipe(
        catchError(this._error.handleError<any>(`getCoffeeProductById`))
      );
  }

  @Cacheable({
    cacheBusterObserver: cacheBuster,
    maxAge: 900000
  })
  getCoffeeTypeById(id: number): Observable<any> {
    return this.http.get<any>(`${environment.webApiUrl}/coffee/types/${id}`)
      .pipe(
        catchError(this._error.handleError<any>(`getCoffeeTypeById`))
      );
  }
}
