export type Priority = 'HIGH' | 'MEDIUM' | 'LOW';

export interface Doctor {
  id: number;
  name: string;
  available_from: string;
  available_until: string;
  created_at?: string;
}

export interface DoctorCreate {
  name: string;
  available_from: string;
  available_until: string;
}

export interface DoctorUpdate {
  name?: string;
  available_from?: string;
  available_until?: string;
}

export interface Room {
  id: number;
  name: string;
  available_from: string;
  available_until: string;
  created_at?: string;
}

export interface RoomCreate {
  name: string;
  available_from: string;
  available_until: string;
}

export interface RoomUpdate {
  name?: string;
  available_from?: string;
  available_until?: string;
}

export interface Patient {
  id: number;
  name: string;
  arrival_time: string;
  priority: Priority;
  consultation_duration: number;
  preferred_doctor_id: number | null;
  created_at?: string;
  preferred_doctor?: Doctor | null;
}

export interface PatientCreate {
  name: string;
  arrival_time: string;
  priority: Priority;
  consultation_duration: number;
  preferred_doctor_id?: number | null;
}

export interface PatientUpdate {
  name?: string;
  arrival_time?: string;
  priority?: Priority;
  consultation_duration?: number;
  preferred_doctor_id?: number | null;
}

export interface Schedule {
  id: number;
  patient_id: number;
  doctor_id: number;
  room_id: number;
  start_time: string;
  end_time: string;
  waiting_time: number;
  created_at?: string;
  patient?: Patient;
  doctor?: Doctor;
  room?: Room;
}

export interface HeuristicBreakdown {
  waiting_time: number;
  conflicts: number;
  priority_penalty: number;
  under_utilization: number;
  waiting_cost: number;
  conflict_cost: number;
  priority_cost: number;
  utilization_cost: number;
  total_score: number;
}

export interface ScheduleGenerationResult {
  success: boolean;
  initial_score: number;
  final_score: number;
  iterations: number;
  improvement: number;
  accepted_moves?: number;
  neighbor_evaluations?: number;
  status_message?: string;
  heuristic: HeuristicBreakdown;
  schedule: Schedule[];
}

export interface ScheduleScoreResponse {
  has_schedule: boolean;
  scheduled_patients?: number;
  message?: string;
  initial_score?: number;
  final_score?: number;
  improvement?: number;
  accepted_moves?: number;
  neighbor_evaluations?: number;
  status_message?: string;
  heuristic?: HeuristicBreakdown;
}


export interface BackendHealth {
  status: string;
  timestamp: string;
  database: {
    status: string;
    patient_count: number;
    doctor_count: number;
    room_count: number;
    scheduled_count: number;
  };
  version: string;
}
