import {
  BackendHealth,
  Doctor,
  DoctorCreate,
  DoctorUpdate,
  Patient,
  PatientCreate,
  PatientUpdate,
  Room,
  RoomCreate,
  RoomUpdate,
  Schedule,
  ScheduleGenerationResult,
  ScheduleScoreResponse
} from '@/types';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

async function handleResponse<T>(res: Response, defaultMessage: string): Promise<T> {
  if (!res.ok) {
    let detail = defaultMessage;
    try {
      const err = await res.json();
      if (err.detail) {
        detail = typeof err.detail === 'string' ? err.detail : JSON.stringify(err.detail);
      }
    } catch {
      detail = `${defaultMessage} (${res.status} ${res.statusText})`;
    }
    throw new Error(detail);
  }
  if (res.status === 204) {
    return {} as T;
  }
  return res.json();
}

// -------------------------------------------------------------
// System Health & Database Reset
// -------------------------------------------------------------
export async function getHealth(): Promise<BackendHealth> {
  const res = await fetch(`${API_BASE_URL}/health`, { cache: 'no-store' });
  return handleResponse<BackendHealth>(res, 'Failed to fetch backend health');
}

export async function resetDatabase(): Promise<{ message: string; patients_count: number; doctors_count: number; rooms_count: number }> {
  const res = await fetch(`${API_BASE_URL}/seed/reset`, {
    method: 'POST',
    cache: 'no-store',
  });
  return handleResponse(res, 'Failed to reset seed database');
}

// -------------------------------------------------------------
// Patients CRUD
// -------------------------------------------------------------
export async function getPatients(): Promise<Patient[]> {
  const res = await fetch(`${API_BASE_URL}/patients`, { cache: 'no-store' });
  return handleResponse<Patient[]>(res, 'Failed to fetch patients');
}

export async function getPatient(id: number): Promise<Patient> {
  const res = await fetch(`${API_BASE_URL}/patients/${id}`, { cache: 'no-store' });
  return handleResponse<Patient>(res, `Failed to fetch patient #${id}`);
}

export async function createPatient(data: PatientCreate): Promise<Patient> {
  const res = await fetch(`${API_BASE_URL}/patients`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<Patient>(res, 'Failed to create patient');
}

export async function updatePatient(id: number, data: PatientUpdate): Promise<Patient> {
  const res = await fetch(`${API_BASE_URL}/patients/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<Patient>(res, `Failed to update patient #${id}`);
}

export async function deletePatient(id: number): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/patients/${id}`, {
    method: 'DELETE',
  });
  return handleResponse<void>(res, `Failed to delete patient #${id}`);
}

// -------------------------------------------------------------
// Doctors CRUD
// -------------------------------------------------------------
export async function getDoctors(): Promise<Doctor[]> {
  const res = await fetch(`${API_BASE_URL}/doctors`, { cache: 'no-store' });
  return handleResponse<Doctor[]>(res, 'Failed to fetch doctors');
}

export async function getDoctor(id: number): Promise<Doctor> {
  const res = await fetch(`${API_BASE_URL}/doctors/${id}`, { cache: 'no-store' });
  return handleResponse<Doctor>(res, `Failed to fetch doctor #${id}`);
}

export async function createDoctor(data: DoctorCreate): Promise<Doctor> {
  const res = await fetch(`${API_BASE_URL}/doctors`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<Doctor>(res, 'Failed to create doctor');
}

export async function updateDoctor(id: number, data: DoctorUpdate): Promise<Doctor> {
  const res = await fetch(`${API_BASE_URL}/doctors/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<Doctor>(res, `Failed to update doctor #${id}`);
}

export async function deleteDoctor(id: number): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/doctors/${id}`, {
    method: 'DELETE',
  });
  return handleResponse<void>(res, `Failed to delete doctor #${id}`);
}

// -------------------------------------------------------------
// Rooms CRUD
// -------------------------------------------------------------
export async function getRooms(): Promise<Room[]> {
  const res = await fetch(`${API_BASE_URL}/rooms`, { cache: 'no-store' });
  return handleResponse<Room[]>(res, 'Failed to fetch rooms');
}

export async function getRoom(id: number): Promise<Room> {
  const res = await fetch(`${API_BASE_URL}/rooms/${id}`, { cache: 'no-store' });
  return handleResponse<Room>(res, `Failed to fetch room #${id}`);
}

export async function createRoom(data: RoomCreate): Promise<Room> {
  const res = await fetch(`${API_BASE_URL}/rooms`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<Room>(res, 'Failed to create room');
}

export async function updateRoom(id: number, data: RoomUpdate): Promise<Room> {
  const res = await fetch(`${API_BASE_URL}/rooms/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  });
  return handleResponse<Room>(res, `Failed to update room #${id}`);
}

export async function deleteRoom(id: number): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/rooms/${id}`, {
    method: 'DELETE',
  });
  return handleResponse<void>(res, `Failed to delete room #${id}`);
}

// -------------------------------------------------------------
// Scheduling & Heuristic Engine
// -------------------------------------------------------------
export async function generateSchedule(): Promise<ScheduleGenerationResult> {
  const res = await fetch(`${API_BASE_URL}/schedule/generate`, {
    method: 'POST',
    cache: 'no-store',
  });
  return handleResponse<ScheduleGenerationResult>(res, 'Failed to generate schedule via Hill Climbing');
}

export async function getSchedule(): Promise<Schedule[]> {
  const res = await fetch(`${API_BASE_URL}/schedule`, { cache: 'no-store' });
  return handleResponse<Schedule[]>(res, 'Failed to fetch schedule');
}

export async function getScheduleScore(): Promise<ScheduleScoreResponse> {
  const res = await fetch(`${API_BASE_URL}/schedule/score`, { cache: 'no-store' });
  return handleResponse<ScheduleScoreResponse>(res, 'Failed to fetch schedule score');
}

export async function deleteScheduleEntry(id: number): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/schedule/${id}`, {
    method: 'DELETE',
  });
  return handleResponse<void>(res, `Failed to delete appointment #${id}`);
}

export async function clearAllSchedules(): Promise<void> {
  const res = await fetch(`${API_BASE_URL}/schedule`, {
    method: 'DELETE',
  });
  return handleResponse<void>(res, 'Failed to clear schedules');
}

