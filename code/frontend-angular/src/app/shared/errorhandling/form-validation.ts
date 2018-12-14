import { IFormValidationObject } from '../interfaces/form-validation-objects';


function validatePassword(password: string): string {
  return password.length < 6 ? 'Das Passwort muss mindestens 6 Zeichen lang sein.' : null;
}

function comparePasswords(password: string, passwordConfirmation: string): string {
  return password !== passwordConfirmation ? 'Die Passwörter stimmen nicht überein.' : null;
}

function validateUserName(userName: string): string {
  return userName.length < 6 ? 'Der Nutzername muss mindestens 6 Zeichen lang sein.' : null;
}

export function validateAccountSettings(password: string, passwordConfirmation: string, userName: string): IFormValidationObject {

  const formValObject: IFormValidationObject = {
    error: false,
    errorMessages: []
  };

  const valPwResult = validatePassword(password);
  const valUnResult = validateUserName(userName);
  const valCmpPwResult = comparePasswords(password, passwordConfirmation);

  if (valPwResult) {
    formValObject.error = true;
    formValObject.errorMessages = [...formValObject.errorMessages, valPwResult];
  }

  if (valUnResult) {
    formValObject.error = true;
    formValObject.errorMessages = [...formValObject.errorMessages, valUnResult];
  }

  if (valCmpPwResult) {
    formValObject.error = true;
    formValObject.errorMessages = [...formValObject.errorMessages, valCmpPwResult];
  }

  return formValObject;
}
