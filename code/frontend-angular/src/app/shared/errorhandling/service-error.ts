import {Observable, of, throwError} from 'rxjs';


export class ServiceError {

  constructor() {}

  public handleError<T> (operation = 'operation', result?: T) {
    return (error: any): Observable<T> => {

      let errorMessage: string;

      if (error.error instanceof ErrorEvent) {
        console.error('A client side error occured:', error.error.message);
        errorMessage = `A client side error occured: ${error.error.message}`;
      } else {
        // distinguish error codes
        switch (error.status) {
          case 400: errorMessage = `Wir haben bei den übermittelten Daten einen Fehler gefunden: ${error.error.message}`; break;
          case 401: errorMessage = `Wir konnten deine Anmeldedaten nicht feststellen.`; break;
          case 403: errorMessage = `Diese Aktion ist nicht verfügbar`; break;
          case 404: errorMessage = `Die angefragte Ressource scheint nicht zu existieren. Überprüfe bitte deine Eingaben`; break;
          case 405: errorMessage = `Das Gerät ist noch nicht bereit. Bitte versuche es später noch einmal`; break;
          default: errorMessage = `Da ist etwas auf unserer Seite schief gelaufen ... versuche es bitte später noch einmal.`;
        }
      }

      // Let the app keep running by returning an empty result.
      // return of(result as T);
      return throwError(errorMessage);
    };
  }
}
