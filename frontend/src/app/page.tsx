'use client';

import React, { useState, useEffect, useCallback } from 'react';
import Link from 'next/link';
import {
  Users,
  Stethoscope,
  Building2,
  CalendarCheck,
  Clock,
  AlertTriangle,
  Brain,
  ArrowRight,
  Sparkles,
  CheckCircle2,
  ChevronRight
} from 'lucide-react';
import AppShell from '@/components/AppShell';
import { getSchedule, getScheduleScore, getPatients } from '@/lib/api';
import { Patient, Schedule, ScheduleScoreResponse } from '@/types';

export default function DashboardPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const [scoreData, setScoreData] = useState<ScheduleScoreResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [patientsRes, schedulesRes, scoreRes] = await Promise.all([
        getPatients().catch(() => []),
        getSchedule().catch(() => []),
        getScheduleScore().catch(() => null)
      ]);
      setPatients(patientsRes);
      setSchedules(schedulesRes);
      setScoreData(scoreRes);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  // Derived metrics from real data
  const totalPatients = patients.length;
  const totalDoctors = 4; // Or distinct doctor IDs
  const totalRooms = 3;   // Or distinct room IDs
  const scheduledCount = schedules.length;

  const totalWaitingTime = scoreData?.heuristic?.waiting_time ?? 
    schedules.reduce((sum, s) => sum + s.waiting_time, 0);

  const avgWaitingTime = scheduledCount > 0 
    ? Math.round((totalWaitingTime / scheduledCount) * 10) / 10 
    : 0;

  const conflicts = scoreData?.heuristic?.conflicts ?? 0;
  const heuristicScore = scoreData?.heuristic?.total_score ?? null;

  const highPriority = patients.filter(p => p.priority === 'HIGH').length;
  const medPriority = patients.filter(p => p.priority === 'MEDIUM').length;
  const lowPriority = patients.filter(p => p.priority === 'LOW').length;

  return (
    <AppShell
      title="Hospital Operations Dashboard"
      subtitle="Overview of patient consultations, resource allocation, and AI optimization status"
      onDataRefresh={loadData}
    >
      {/* Welcome & Algorithm Overview Hero */}
      <div className="rounded-2xl bg-gradient-to-r from-blue-900 via-indigo-900 to-slate-900 text-white p-6 sm:p-7 shadow-lg relative overflow-hidden">
        <div className="relative z-10 max-w-3xl space-y-3">
          <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-500/20 border border-blue-400/30 text-blue-300 text-xs font-semibold uppercase tracking-wider">
            <Sparkles className="h-3.5 w-3.5" />
            AI Heuristic Optimization Engine
          </div>
          <h2 className="text-xl sm:text-2xl font-bold tracking-tight">
            Consultation Scheduling with Hill Climbing
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            Minimizes patient waiting time, prevents doctor and room double-booking, guarantees emergency priority handling, and maximizes clinical resource utilization across the 09:00 AM – 01:00 PM operating window.
          </p>

          <div className="pt-2 flex flex-wrap gap-2 text-xs">
            <span className="font-mono bg-white/10 px-2.5 py-1 rounded-md border border-white/10 text-blue-200">
              H(S) = 5(WT) + 100(C) + 20(P) + 10(U)
            </span>
          </div>
        </div>
      </div>

      {/* Primary Metrics Grid (8 cards) */}
      <div className="grid grid-cols-2 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        {/* Total Patients */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs hover:border-slate-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Patients</span>
            <div className="h-8 w-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
              <Users className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-2 text-2xl font-bold text-slate-900">
            {loading ? '...' : totalPatients}
          </div>
          <div className="mt-1 text-[11px] text-slate-500 flex gap-1">
            <span className="text-rose-600 font-semibold">{highPriority} High</span> &bull;{' '}
            <span className="text-amber-600 font-semibold">{medPriority} Med</span> &bull;{' '}
            <span className="text-emerald-600 font-semibold">{lowPriority} Low</span>
          </div>
        </div>

        {/* Total Doctors */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs hover:border-slate-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Active Doctors</span>
            <div className="h-8 w-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
              <Stethoscope className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-2 text-2xl font-bold text-slate-900">
            {loading ? '...' : totalDoctors}
          </div>
          <div className="mt-1 text-[11px] text-slate-500">
            Shift: 09:00 - 13:00 (4h)
          </div>
        </div>

        {/* Total Rooms */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs hover:border-slate-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Consultation Rooms</span>
            <div className="h-8 w-8 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center">
              <Building2 className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-2 text-2xl font-bold text-slate-900">
            {loading ? '...' : totalRooms}
          </div>
          <div className="mt-1 text-[11px] text-slate-500">
            Hours: 09:00 - 13:00 (4h)
          </div>
        </div>

        {/* Scheduled Patients */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs hover:border-slate-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Scheduled</span>
            <div className="h-8 w-8 rounded-lg bg-emerald-50 text-emerald-600 flex items-center justify-center">
              <CalendarCheck className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-2 text-2xl font-bold text-slate-900">
            {loading ? '...' : `${scheduledCount} / ${totalPatients}`}
          </div>
          <div className="mt-1 text-[11px] text-emerald-600 font-semibold flex items-center gap-1">
            {scheduledCount === totalPatients && totalPatients > 0 ? (
              <>
                <CheckCircle2 className="h-3 w-3" /> All patients assigned
              </>
            ) : (
              <span className="text-amber-600">Pending optimization</span>
            )}
          </div>
        </div>

        {/* Total Waiting Time */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs hover:border-slate-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Total Wait Time</span>
            <div className="h-8 w-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
              <Clock className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-2 text-2xl font-bold text-slate-900">
            {loading ? '...' : `${totalWaitingTime} min`}
          </div>
          <div className="mt-1 text-[11px] text-slate-500">
            Weighted Cost: 5 &times; {totalWaitingTime} = {totalWaitingTime * 5}
          </div>
        </div>

        {/* Average Waiting Time */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs hover:border-slate-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Avg Wait Time</span>
            <div className="h-8 w-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center">
              <Clock className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-2 text-2xl font-bold text-slate-900">
            {loading ? '...' : `${avgWaitingTime} min`}
          </div>
          <div className="mt-1 text-[11px] text-slate-500">
            Per consultation
          </div>
        </div>

        {/* Conflicts */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs hover:border-slate-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Conflicts</span>
            <div className={`h-8 w-8 rounded-lg flex items-center justify-center ${
              conflicts > 0 ? 'bg-rose-50 text-rose-600' : 'bg-emerald-50 text-emerald-600'
            }`}>
              <AlertTriangle className="h-4 w-4" />
            </div>
          </div>
          <div className={`mt-2 text-2xl font-bold ${conflicts > 0 ? 'text-rose-600' : 'text-emerald-700'}`}>
            {loading ? '...' : conflicts}
          </div>
          <div className="mt-1 text-[11px] text-slate-500">
            Penalty Weight: 100 &times; {conflicts} = {conflicts * 100}
          </div>
        </div>

        {/* Current Heuristic Score */}
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs hover:border-slate-300 transition">
          <div className="flex items-center justify-between">
            <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider">Heuristic H(S)</span>
            <div className="h-8 w-8 rounded-lg bg-indigo-50 text-indigo-600 flex items-center justify-center">
              <Brain className="h-4 w-4" />
            </div>
          </div>
          <div className="mt-2 text-2xl font-bold font-mono text-indigo-900">
            {loading ? '...' : heuristicScore !== null ? heuristicScore : '--'}
          </div>
          <div className="mt-1 text-[11px] text-slate-500">
            Minimization score (lower is better)
          </div>
        </div>
      </div>

      {/* Quick Navigation Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        {/* Schedule View Card */}
        <Link
          href="/schedule"
          className="p-5 rounded-xl border border-slate-200 bg-white hover:border-blue-300 hover:shadow-sm transition group"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-blue-600 flex items-center gap-1.5">
              <CalendarCheck className="h-4 w-4" /> Schedule &amp; Timeline
            </span>
            <ChevronRight className="h-4 w-4 text-slate-400 group-hover:text-blue-600 group-hover:translate-x-0.5 transition" />
          </div>
          <h3 className="text-sm font-bold text-slate-900 mt-2">
            Detailed Appointment Timeline
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            Filter appointments by doctor, room, and priority. Inspect scheduled start/end times and patient wait durations.
          </p>
        </Link>

        {/* Heuristic Breakdown Card */}
        <Link
          href="/heuristic"
          className="p-5 rounded-xl border border-slate-200 bg-white hover:border-indigo-300 hover:shadow-sm transition group"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-indigo-600 flex items-center gap-1.5">
              <Brain className="h-4 w-4" /> Heuristic Analysis
            </span>
            <ChevronRight className="h-4 w-4 text-slate-400 group-hover:text-indigo-600 group-hover:translate-x-0.5 transition" />
          </div>
          <h3 className="text-sm font-bold text-slate-900 mt-2">
            Objective Function Breakdown
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            Analyze waiting cost, conflict cost, priority penalty, under-utilization, and examine the assignment reference example.
          </p>
        </Link>

        {/* Patient Management Card */}
        <Link
          href="/patients"
          className="p-5 rounded-xl border border-slate-200 bg-white hover:border-emerald-300 hover:shadow-sm transition group"
        >
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold uppercase tracking-wider text-emerald-600 flex items-center gap-1.5">
              <Users className="h-4 w-4" /> Patient Roster
            </span>
            <ChevronRight className="h-4 w-4 text-slate-400 group-hover:text-emerald-600 group-hover:translate-x-0.5 transition" />
          </div>
          <h3 className="text-sm font-bold text-slate-900 mt-2">
            Patient CRUD &amp; Triage
          </h3>
          <p className="text-xs text-slate-500 mt-1">
            Add, update, or remove patients. Configure arrival times, consultation durations (10–30m), and preferred doctors.
          </p>
        </Link>
      </div>

      {/* Schedule Preview Section */}
      <div className="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-2xs">
        <div className="px-6 py-4 border-b border-slate-100 flex items-center justify-between flex-wrap gap-2">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Current Consultation Schedule</h3>
            <p className="text-xs text-slate-500">Preview of active appointments stored in SQLite</p>
          </div>
          <Link
            href="/schedule"
            className="text-xs font-semibold text-blue-600 hover:text-blue-700 flex items-center gap-1"
          >
            Open Full Schedule View <ArrowRight className="h-3.5 w-3.5" />
          </Link>
        </div>

        {schedules.length === 0 ? (
          <div className="p-12 text-center text-slate-500">
            <Clock className="h-8 w-8 text-slate-300 mx-auto mb-2" />
            <p className="text-xs font-semibold text-slate-700">No schedule generated yet</p>
            <p className="text-xs text-slate-400 mt-1">
              Click &quot;Generate Schedule&quot; in the header to run Hill Climbing optimization.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider">
                <tr>
                  <th className="py-2.5 px-4">Time Slot</th>
                  <th className="py-2.5 px-4">Patient</th>
                  <th className="py-2.5 px-4">Priority</th>
                  <th className="py-2.5 px-4">Assigned Doctor</th>
                  <th className="py-2.5 px-4">Assigned Room</th>
                  <th className="py-2.5 px-4">Arrival</th>
                  <th className="py-2.5 px-4">Wait Time</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {schedules.slice(0, 8).map((s) => (
                  <tr key={s.id} className="hover:bg-slate-50/80 transition">
                    <td className="py-2.5 px-4 font-mono font-bold text-blue-700">
                      {s.start_time} - {s.end_time}
                    </td>
                    <td className="py-2.5 px-4 font-semibold text-slate-900">
                      {s.patient?.name || `Patient #${s.patient_id}`}
                    </td>
                    <td className="py-2.5 px-4">
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded text-[10px] font-bold ${
                          s.patient?.priority === 'HIGH'
                            ? 'bg-rose-100 text-rose-700 border border-rose-200'
                            : s.patient?.priority === 'MEDIUM'
                            ? 'bg-amber-100 text-amber-700 border border-amber-200'
                            : 'bg-emerald-100 text-emerald-700 border border-emerald-200'
                        }`}
                      >
                        {s.patient?.priority || 'MEDIUM'}
                      </span>
                    </td>
                    <td className="py-2.5 px-4 font-medium text-slate-800">
                      {s.doctor?.name || `Doctor #${s.doctor_id}`}
                    </td>
                    <td className="py-2.5 px-4 font-medium text-slate-800">
                      {s.room?.name || `Room #${s.room_id}`}
                    </td>
                    <td className="py-2.5 px-4 font-mono text-slate-500">
                      {s.patient?.arrival_time || '--:--'}
                    </td>
                    <td className="py-2.5 px-4">
                      <span className={`font-mono font-semibold ${s.waiting_time > 20 ? 'text-amber-600' : 'text-slate-700'}`}>
                        {s.waiting_time} min
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
            {schedules.length > 8 && (
              <div className="p-3 bg-slate-50/70 border-t border-slate-100 text-center text-xs text-slate-500">
                Showing 8 of {schedules.length} scheduled consultations &bull;{' '}
                <Link href="/schedule" className="text-blue-600 hover:underline font-semibold">
                  View all in Schedule tab
                </Link>
              </div>
            )}
          </div>
        )}
      </div>
    </AppShell>
  );
}
