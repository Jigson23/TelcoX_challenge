// Author: Ing. Jigson Contreras
// Email: supercontreras-ji@hotmail.com
import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable, forkJoin, map } from 'rxjs';

import { environment } from '../../../environments/environment';

export interface CustomerProfile {
  cliente_id: string;
  nombre: string;
  saldo: number;
  consumo_mb: number;
  minutos: number;
}

export interface ConsumptionSummary {
  cliente_id: string;
  consumo_mb: number;
  minutos: number;
}

export interface DashboardData {
  profile: CustomerProfile;
  consumption: ConsumptionSummary;
}

@Injectable({ providedIn: 'root' })
export class ConsumptionService {
  private readonly apiUrl = environment.apiUrl;

  constructor(private readonly http: HttpClient) {}

  getCustomerProfile(customerId: string): Observable<CustomerProfile> {
    const params = new HttpParams().set('customer_id', customerId);
    return this.http.get<CustomerProfile>(`${this.apiUrl}/api/cliente`, { params });
  }

  getConsumption(customerId: string): Observable<ConsumptionSummary> {
    const params = new HttpParams().set('customer_id', customerId);
    return this.http.get<ConsumptionSummary>(`${this.apiUrl}/api/consumo`, { params });
  }

  getDashboardData(customerId: string): Observable<DashboardData> {
    return forkJoin({
      profile: this.getCustomerProfile(customerId),
      consumption: this.getConsumption(customerId)
    }).pipe(
      map(({ profile, consumption }) => ({
        profile,
        consumption: {
          cliente_id: consumption.cliente_id,
          consumo_mb: consumption.consumo_mb,
          minutos: consumption.minutos
        }
      }))
    );
  }
}
