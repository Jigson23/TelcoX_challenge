import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';

import {
  ConsumptionService,
  ConsumptionSummary,
  CustomerProfile,
  DashboardData
} from './consumption.service';

describe('ConsumptionService', () => {
  let service: ConsumptionService;
  let httpMock: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule]
    });

    service = TestBed.inject(ConsumptionService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should request the customer profile endpoint', () => {
    const mockProfile: CustomerProfile = {
      cliente_id: '0001',
      nombre: 'Ana Pérez',
      saldo: 15.5,
      consumo_mb: 1024,
      minutos: 120
    };

    service.getCustomerProfile('0001').subscribe((profile) => {
      expect(profile).toEqual(mockProfile);
    });

    const request = httpMock.expectOne('http://localhost:5000/api/cliente?customer_id=0001');
    expect(request.request.method).toBe('GET');
    request.flush(mockProfile);
  });

  it('should request the consumption endpoint', () => {
    const mockConsumption: ConsumptionSummary = {
      cliente_id: '0002',
      consumo_mb: 5120,
      minutos: 45
    };

    service.getConsumption('0002').subscribe((consumption) => {
      expect(consumption).toEqual(mockConsumption);
    });

    const request = httpMock.expectOne('http://localhost:5000/api/consumo?customer_id=0002');
    expect(request.request.method).toBe('GET');
    request.flush(mockConsumption);
  });

  it('should merge profile and consumption data for the dashboard', () => {
    const mockProfile: CustomerProfile = {
      cliente_id: '0003',
      nombre: 'María López',
      saldo: 0,
      consumo_mb: 256,
      minutos: 300
    };
    const mockConsumption: ConsumptionSummary = {
      cliente_id: '0003',
      consumo_mb: 256,
      minutos: 300
    };

    service.getDashboardData('0003').subscribe((data: DashboardData) => {
      expect(data).toEqual({
        profile: mockProfile,
        consumption: mockConsumption
      });
    });

    const profileRequest = httpMock.expectOne('http://localhost:5000/api/cliente?customer_id=0003');
    const consumptionRequest = httpMock.expectOne('http://localhost:5000/api/consumo?customer_id=0003');

    profileRequest.flush(mockProfile);
    consumptionRequest.flush(mockConsumption);
  });

  it('should propagate errors when one of the API calls fails', () => {
    const mockProfile: CustomerProfile = {
      cliente_id: '0004',
      nombre: 'Cliente Demo',
      saldo: 10,
      consumo_mb: 100,
      minutos: 20
    };

    service.getDashboardData('0004').subscribe({
      next: () => fail('La llamada debería haber fallado'),
      error: (error) => {
        expect(error.status).toBe(500);
      }
    });

    const profileRequest = httpMock.expectOne('http://localhost:5000/api/cliente?customer_id=0004');
    const consumptionRequest = httpMock.expectOne('http://localhost:5000/api/consumo?customer_id=0004');

    profileRequest.flush(mockProfile);
    consumptionRequest.flush(
      { mensaje: 'Fallo del servicio' },
      { status: 500, statusText: 'Server Error' }
    );
  });
});
