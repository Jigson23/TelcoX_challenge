// Author: Ing. Jigson Contreras
// Email: supercontreras-ji@hotmail.com
import { inject } from '@angular/core';
import { HttpErrorResponse, HttpInterceptorFn } from '@angular/common/http';
import { MessageService } from 'primeng/api';
import { catchError, throwError } from 'rxjs';

export const errorInterceptor: HttpInterceptorFn = (req, next) => {
  const messageService = inject(MessageService);

  return next(req).pipe(
    catchError((error: HttpErrorResponse) => {
      const detail =
        (error.error && (error.error.mensaje || error.error.detail)) ||
        error.message ||
        'Ocurrió un error inesperado al procesar la solicitud.';

      messageService.add({ severity: 'error', summary: 'Error', detail });
      return throwError(() => error);
    })
  );
};
