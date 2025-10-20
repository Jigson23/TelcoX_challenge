// Author: Ing. Jigson Contreras
// Email: supercontreras-ji@hotmail.com
import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';
import { ReactiveFormsModule } from '@angular/forms';

import { CardModule } from 'primeng/card';
import { TableModule } from 'primeng/table';
import { ToastModule } from 'primeng/toast';
import { InputTextModule } from 'primeng/inputtext';
import { ButtonModule } from 'primeng/button';
import { ProgressSpinnerModule } from 'primeng/progressspinner';

import { ConsumptionDashboardComponent } from './components/consumption-dashboard/consumption-dashboard.component';

const routes: Routes = [
  {
    path: '',
    component: ConsumptionDashboardComponent
  }
];

@NgModule({
  declarations: [ConsumptionDashboardComponent],
  imports: [
    CommonModule,
    RouterModule.forChild(routes),
    ReactiveFormsModule,
    CardModule,
    TableModule,
    ToastModule,
    InputTextModule,
    ButtonModule,
    ProgressSpinnerModule
  ]
})
export class ConsumptionModule {}
