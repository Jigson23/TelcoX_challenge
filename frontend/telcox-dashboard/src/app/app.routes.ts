import { Routes } from '@angular/router';

export const routes: Routes = [
  {
    path: '',
    loadChildren: () =>
      import('./consumption/consumption.module').then((m) => m.ConsumptionModule)
  },
  {
    path: '**',
    redirectTo: ''
  }
];
