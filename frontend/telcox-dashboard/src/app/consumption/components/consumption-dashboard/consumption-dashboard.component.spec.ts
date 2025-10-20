// Author: Ing. Jigson Contreras
// Email: supercontreras-ji@hotmail.com
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ReactiveFormsModule } from '@angular/forms';
import { of, throwError } from 'rxjs';
import { MessageService } from 'primeng/api';

import { ConsumptionDashboardComponent } from './consumption-dashboard.component';
import { ConsumptionService, DashboardData } from '../../services/consumption.service';

describe('ConsumptionDashboardComponent', () => {
  let component: ConsumptionDashboardComponent;
  let fixture: ComponentFixture<ConsumptionDashboardComponent>;
  let service: jasmine.SpyObj<ConsumptionService>;
  let messageService: jasmine.SpyObj<MessageService>;

  const dashboardData: DashboardData = {
    profile: {
      cliente_id: '0001',
      nombre: 'Ana Pérez',
      saldo: 15.5,
      consumo_mb: 1024,
      minutos: 120
    },
    consumption: {
      cliente_id: '0001',
      consumo_mb: 1024,
      minutos: 120
    }
  };

  beforeEach(async () => {
    service = jasmine.createSpyObj('ConsumptionService', ['getDashboardData']);
    messageService = jasmine.createSpyObj('MessageService', ['add']);

    await TestBed.configureTestingModule({
      imports: [ReactiveFormsModule],
      declarations: [ConsumptionDashboardComponent],
      providers: [
        { provide: ConsumptionService, useValue: service },
        { provide: MessageService, useValue: messageService }
      ],
      schemas: [NO_ERRORS_SCHEMA]
    }).compileComponents();

    fixture = TestBed.createComponent(ConsumptionDashboardComponent);
    component = fixture.componentInstance;
  });

  it('should load dashboard data on init and build rows', () => {
    service.getDashboardData.and.returnValue(of(dashboardData));

    fixture.detectChanges();

    expect(service.getDashboardData).toHaveBeenCalledWith('0001');
    expect(component.loading).toBeFalse();
    expect(component.data).toEqual(dashboardData);
    expect(component.consumptionRows.length).toBe(3);
    expect(messageService.add).toHaveBeenCalledWith(
      jasmine.objectContaining({ severity: 'success', summary: 'Datos actualizados' })
    );
  });

  it('should clear data when the service emits an error', () => {
    service.getDashboardData.and.returnValue(throwError(() => new Error('Fallo')));

    fixture.detectChanges();

    expect(component.loading).toBeFalse();
    expect(component.data).toBeUndefined();
    expect(component.consumptionRows).toEqual([]);
    expect(messageService.add).not.toHaveBeenCalled();
  });

  it('should not call the service when the form is invalid', () => {
    service.getDashboardData.and.returnValue(of(dashboardData));
    component.customerForm.controls.customerId.setValue('');

    component.loadDashboard();

    expect(component.customerForm.touched).toBeTrue();
    expect(service.getDashboardData).not.toHaveBeenCalled();
  });
});
