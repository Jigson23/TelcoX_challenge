import { Component, OnInit } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { finalize } from 'rxjs';
import { MessageService } from 'primeng/api';

import { ConsumptionService, DashboardData } from '../../services/consumption.service';

interface ConsumptionRow {
  metric: string;
  value: string;
  description?: string;
}

@Component({
  selector: 'app-consumption-dashboard',
  templateUrl: './consumption-dashboard.component.html',
  styleUrls: ['./consumption-dashboard.component.scss']
})
export class ConsumptionDashboardComponent implements OnInit {
  readonly customerForm: FormGroup<{ customerId: FormControl<string> }>;

  loading = false;
  data?: DashboardData;
  consumptionRows: ConsumptionRow[] = [];

  constructor(
    private readonly fb: FormBuilder,
    private readonly consumptionService: ConsumptionService,
    private readonly messageService: MessageService
  ) {
    this.customerForm = this.fb.nonNullable.group({
      customerId: ['0001', [Validators.required, Validators.minLength(4)]]
    });
  }

  ngOnInit(): void {
    this.loadDashboard();
  }

  loadDashboard(): void {
    if (this.customerForm.invalid) {
      this.customerForm.markAllAsTouched();
      return;
    }

    const customerId = this.customerForm.controls.customerId.value.trim();
    if (!customerId) {
      return;
    }

    this.loading = true;
    this.consumptionService
      .getDashboardData(customerId)
      .pipe(finalize(() => (this.loading = false)))
      .subscribe({
        next: (response) => {
          this.data = response;
          this.consumptionRows = this.buildRows(response);
          this.messageService.add({
            severity: 'success',
            summary: 'Datos actualizados',
            detail: `Información del cliente ${response.profile.nombre}`
          });
        },
        error: () => {
          this.data = undefined;
          this.consumptionRows = [];
        }
      });
  }

  private buildRows(data: DashboardData): ConsumptionRow[] {
    return [
      {
        metric: 'Saldo disponible',
        value: new Intl.NumberFormat('es-EC', {
          style: 'currency',
          currency: 'USD',
          currencyDisplay: 'narrowSymbol'
        }).format(data.profile.saldo),
        description: 'Crédito actual en la cuenta.'
      },
      {
        metric: 'Datos consumidos',
        value: `${data.consumption.consumo_mb.toLocaleString('es-EC')} MB`,
        description: 'Total de megabytes utilizados en el periodo.'
      },
      {
        metric: 'Minutos utilizados',
        value: data.consumption.minutos.toLocaleString('es-EC'),
        description: 'Tiempo total de llamadas registradas.'
      }
    ];
  }
}
