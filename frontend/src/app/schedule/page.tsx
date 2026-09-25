'use client';

import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  CalendarDays,
  Search,
  Trash2,
  AlertCircle,
  CheckCircle2
} from 'lucide-react';
import AppShell from '@/components/AppShell';
import ConfirmDeleteModal from '@/components/ConfirmDeleteModal';
import {
  getSchedule,
  getDoctors,
  getRooms,
  getScheduleScore,
  deleteScheduleEntry,
  clearAllSchedules
} from '@/lib/api';
import { Schedule, Doctor, Room, ScheduleScoreResponse } from '@/types';


export default function SchedulePage() {
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [scoreData, setScoreData] = useState<ScheduleScoreResponse | null>(null);
  const [loading, setLoading] = useState(true);

  // Delete State
  const [entryToDelete, setEntryToDelete] = useState<Schedule | null>(null);
  const [isClearAllModalOpen, setIsClearAllModalOpen] = useState(false);
  const [isDeleting, setIsDeleting] = useState(false);
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  // Filters
  const [selectedDoctor, setSelectedDoctor] = useState<string>('ALL');
  const [selectedRoom, setSelectedRoom] = useState<string>('ALL');
  const [selectedPriority, setSelectedPriority] = useState<string>('ALL');
  const [searchQuery, setSearchQuery] = useState('');

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [schedRes, docsRes, roomsRes, scoreRes] = await Promise.all([
        getSchedule(),
        getDoctors().catch(() => []),
        getRooms().catch(() => []),
        getScheduleScore().catch(() => null)
      ]);
      setSchedules(schedRes);
      setDoctors(docsRes);
      setRooms(roomsRes);
      setScoreData(scoreRes);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleConfirmDeleteEntry = async () => {
    if (!entryToDelete) return;
    try {
      setIsDeleting(true);
      await deleteScheduleEntry(entryToDelete.id);
      setNotification({
        type: 'success',
        message: `Appointment for "${entryToDelete.patient?.name || `Patient #${entryToDelete.patient_id}`}" has been cancelled.`,
      });
      setEntryToDelete(null);
      await loadData();
    } catch (err: unknown) {
      setNotification({
        type: 'error',
        message: err instanceof Error ? err.message : 'Failed to cancel appointment',
      });
      setEntryToDelete(null);
    } finally {
      setIsDeleting(false);
    }
  };

  const handleConfirmClearAll = async () => {
    try {
      setIsDeleting(true);
      await clearAllSchedules();
      setNotification({
        type: 'success',
        message: 'All scheduled appointments have been cleared.',
      });
      setIsClearAllModalOpen(false);
      await loadData();
    } catch (err: unknown) {
      setNotification({
        type: 'error',
        message: err instanceof Error ? err.message : 'Failed to clear schedules',
      });
      setIsClearAllModalOpen(false);
    } finally {
      setIsDeleting(false);
    }
  };


  // Filtered & sorted schedules
  const filteredSchedules = useMemo(() => {
    return schedules
      .filter((s) => {
        const matchesDoc = selectedDoctor === 'ALL' || s.doctor_id === Number(selectedDoctor);
        const matchesRoom = selectedRoom === 'ALL' || s.room_id === Number(selectedRoom);
        const matchesPriority = selectedPriority === 'ALL' || s.patient?.priority === selectedPriority;
        const matchesSearch = !searchQuery.trim() || 
          (s.patient?.name.toLowerCase().includes(searchQuery.toLowerCase()) ?? false);
        return matchesDoc && matchesRoom && matchesPriority && matchesSearch;
      })
      .sort((a, b) => {
        // Sort by start_time
        return a.start_time.localeCompare(b.start_time);
      });
  }, [schedules, selectedDoctor, selectedRoom, selectedPriority, searchQuery]);

  // Metrics
  const totalScheduled = schedules.length;
  const totalWait = scoreData?.heuristic?.waiting_time ?? 
    schedules.reduce((acc, s) => acc + s.waiting_time, 0);
  const avgWait = totalScheduled > 0 ? Math.round((totalWait / totalScheduled) * 10) / 10 : 0;
  const conflicts = scoreData?.heuristic?.conflicts ?? 0;

  // Timeline helper: convert HH:MM to minutes from midnight
  const parseMin = (hhmm: string): number => {
    const [h, m] = hhmm.split(':').map(Number);
    return h * 60 + m;
  };

  // Timeline Operating Window: 09:00 (540m) to 13:00 (780m) = 240 mins total
  const WINDOW_START = 540;
  const WINDOW_DURATION = 240;

  // Time hour marks for timeline header
  const timelineMarks = ['09:00', '09:30', '10:00', '10:30', '11:00', '11:30', '12:00', '12:30', '13:00'];

  return (
    <AppShell
      title="Consultation Schedule"
      subtitle="Visual timetable, interval timeline, and appointment allocation details"
      onDataRefresh={loadData}
    >
      {/* Metrics Banner */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">
            Scheduled Patients
          </span>
          <div className="mt-1 text-2xl font-bold text-slate-900">{totalScheduled}</div>
          <span className="text-[11px] text-slate-400">Consultations assigned</span>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">
            Total Waiting Time
          </span>
          <div className="mt-1 text-2xl font-bold text-blue-600">{totalWait} min</div>
          <span className="text-[11px] text-slate-400">Summed patient delay</span>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">
            Average Wait Time
          </span>
          <div className="mt-1 text-2xl font-bold text-teal-600">{avgWait} min</div>
          <span className="text-[11px] text-slate-400">Per patient consultation</span>
        </div>

        <div className="bg-white rounded-xl border border-slate-200 p-4 shadow-2xs">
          <span className="text-xs font-semibold text-slate-500 uppercase tracking-wider block">
            Scheduling Conflicts
          </span>
          <div className={`mt-1 text-2xl font-bold ${conflicts > 0 ? 'text-rose-600' : 'text-emerald-600'}`}>
            {conflicts}
          </div>
          <span className="text-[11px] text-slate-400">
            {conflicts === 0 ? '0 Overlaps (Valid Schedule)' : `${conflicts} overlaps detected!`}
          </span>
        </div>
      </div>

      {/* Visual Timeline Section */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-2xs p-5 overflow-hidden">
        <div className="flex items-center justify-between pb-3 border-b border-slate-100 flex-wrap gap-2">
          <div>
            <h3 className="text-sm font-bold text-slate-900">Doctor Consultation Timeline</h3>
            <p className="text-xs text-slate-500">
              Operating hours (09:00 AM - 01:00 PM) mapped by physician
            </p>
          </div>
          <div className="flex items-center gap-3 text-[11px]">
            <span className="flex items-center gap-1 font-semibold text-rose-700">
              <span className="h-2.5 w-2.5 rounded-sm bg-rose-500" /> HIGH
            </span>
            <span className="flex items-center gap-1 font-semibold text-amber-700">
              <span className="h-2.5 w-2.5 rounded-sm bg-amber-500" /> MEDIUM
            </span>
            <span className="flex items-center gap-1 font-semibold text-emerald-700">
              <span className="h-2.5 w-2.5 rounded-sm bg-emerald-500" /> LOW
            </span>
          </div>
        </div>

        {schedules.length === 0 ? (
          <div className="py-8 text-center text-xs text-slate-400">
            Generate a schedule to view the appointment timeline.
          </div>
        ) : (
          <div className="mt-4 overflow-x-auto">
            <div className="min-w-[720px]">
              {/* Timeline Header (Hour Marks) */}
              <div className="grid grid-cols-8 text-[11px] font-mono text-slate-400 pl-40 pr-2 pb-2 border-b border-slate-100">
                {timelineMarks.map((time, idx) => (
                  <span key={idx} className={idx === 0 ? 'text-left' : idx === 8 ? 'text-right' : 'text-center'}>
                    {time}
                  </span>
                ))}
              </div>

              {/* Doctor Rows */}
              <div className="divide-y divide-slate-100 mt-2">
                {doctors.map((doc) => {
                  const docAppts = schedules.filter((s) => s.doctor_id === doc.id);
                  return (
                    <div key={doc.id} className="py-3 flex items-center group">
                      {/* Doctor Label */}
                      <div className="w-40 shrink-0 pr-3">
                        <div className="text-xs font-bold text-slate-800 truncate" title={doc.name}>
                          {doc.name}
                        </div>
                        <div className="text-[10px] text-slate-400">{docAppts.length} consultations</div>
                      </div>

                      {/* Timeline Bar Track */}
                      <div className="flex-1 relative h-9 bg-slate-50 rounded-lg border border-slate-200/80 overflow-hidden">
                        {/* 30-minute guide lines */}
                        {[...Array(7)].map((_, i) => (
                          <div
                            key={i}
                            className="absolute top-0 bottom-0 border-r border-slate-200/50"
                            style={{ left: `${((i + 1) * 30 / WINDOW_DURATION) * 100}%` }}
                          />
                        ))}

                        {/* Consultation Blocks */}
                        {docAppts.map((appt) => {
                          const startM = parseMin(appt.start_time);
                          const endM = parseMin(appt.end_time);
                          const dur = endM - startM;
                          const leftPct = Math.max(0, ((startM - WINDOW_START) / WINDOW_DURATION) * 100);
                          const widthPct = Math.min(100 - leftPct, (dur / WINDOW_DURATION) * 100);

                          const prio = appt.patient?.priority || 'MEDIUM';
                          const bgClass =
                            prio === 'HIGH'
                              ? 'bg-rose-500 hover:bg-rose-600 text-white'
                              : prio === 'MEDIUM'
                              ? 'bg-amber-500 hover:bg-amber-600 text-white'
                              : 'bg-emerald-500 hover:bg-emerald-600 text-white';

                          return (
                            <div
                              key={appt.id}
                              className={`absolute top-1 bottom-1 rounded-md px-1.5 py-0.5 text-[10px] font-semibold flex items-center justify-between overflow-hidden shadow-2xs transition cursor-pointer ${bgClass}`}
                              style={{
                                left: `${leftPct}%`,
                                width: `${widthPct}%`,
                              }}
                              title={`${appt.patient?.name || 'Patient'} (${appt.start_time} - ${appt.end_time}) | Room: ${appt.room?.name || appt.room_id} | Wait: ${appt.waiting_time}m`}
                            >
                              <span className="truncate">{appt.patient?.name?.split(' ')[0] || `P#${appt.patient_id}`}</span>
                              <span className="text-[9px] opacity-80 hidden sm:inline">{dur}m</span>
                            </div>
                          );
                        })}
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Filter and Search Bar */}
      <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 bg-white p-4 rounded-xl border border-slate-200 shadow-2xs">
        {/* Search */}
        <div className="relative flex-1 min-w-[200px]">
          <Search className="h-4 w-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
          <input
            type="text"
            placeholder="Filter by patient name..."
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-200 focus:outline-hidden focus:border-blue-500"
          />
        </div>

        {/* Filter Dropdowns */}
        <div className="flex items-center gap-2 flex-wrap text-xs">
          {/* Doctor Filter */}
          <select
            value={selectedDoctor}
            onChange={(e) => setSelectedDoctor(e.target.value)}
            className="py-1.5 px-2.5 rounded-lg border border-slate-200 bg-white text-slate-700 focus:outline-hidden focus:border-blue-500"
          >
            <option value="ALL">All Doctors</option>
            {doctors.map((d) => (
              <option key={d.id} value={d.id}>
                {d.name}
              </option>
            ))}
          </select>

          {/* Room Filter */}
          <select
            value={selectedRoom}
            onChange={(e) => setSelectedRoom(e.target.value)}
            className="py-1.5 px-2.5 rounded-lg border border-slate-200 bg-white text-slate-700 focus:outline-hidden focus:border-blue-500"
          >
            <option value="ALL">All Rooms</option>
            {rooms.map((r) => (
              <option key={r.id} value={r.id}>
                {r.name}
              </option>
            ))}
          </select>

          {/* Priority Filter */}
          <select
            value={selectedPriority}
            onChange={(e) => setSelectedPriority(e.target.value)}
            className="py-1.5 px-2.5 rounded-lg border border-slate-200 bg-white text-slate-700 focus:outline-hidden focus:border-blue-500"
          >
            <option value="ALL">All Priorities</option>
            <option value="HIGH">HIGH Priority</option>
            <option value="MEDIUM">MEDIUM Priority</option>
            <option value="LOW">LOW Priority</option>
          </select>
        </div>
      </div>

      {/* Action Notification Banner */}
      {notification && (
        <div
          className={`p-3.5 rounded-xl border flex items-center justify-between text-xs font-medium transition ${
            notification.type === 'success'
              ? 'bg-emerald-50 border-emerald-200 text-emerald-800'
              : 'bg-rose-50 border-rose-200 text-rose-800'
          }`}
        >
          <div className="flex items-center gap-2">
            {notification.type === 'success' ? (
              <CheckCircle2 className="h-4 w-4 text-emerald-600 shrink-0" />
            ) : (
              <AlertCircle className="h-4 w-4 text-rose-600 shrink-0" />
            )}
            <span>{notification.message}</span>
          </div>
          <button
            onClick={() => setNotification(null)}
            className="ml-4 font-bold hover:underline shrink-0 cursor-pointer"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* Schedule Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
        <div className="px-6 py-3.5 border-b border-slate-100 flex items-center justify-between flex-wrap gap-2">
          <div>
            <span className="text-xs font-bold text-slate-700 uppercase tracking-wider block">
              Appointment Records ({filteredSchedules.length} of {schedules.length})
            </span>
            <span className="text-xs text-slate-400">Sorted chronologically by consultation start time</span>
          </div>
          {schedules.length > 0 && (
            <button
              onClick={() => setIsClearAllModalOpen(true)}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg border border-rose-200 text-rose-600 hover:bg-rose-50 text-xs font-semibold transition cursor-pointer"
              title="Clear all scheduled appointments"
            >
              <Trash2 className="h-3.5 w-3.5" />
              <span>Clear Schedule</span>
            </button>
          )}
        </div>

        {loading ? (
          <div className="p-12 text-center text-xs text-slate-400">Loading schedule records...</div>
        ) : filteredSchedules.length === 0 ? (
          <div className="p-12 text-center text-slate-500">
            <CalendarDays className="h-8 w-8 text-slate-300 mx-auto mb-2" />
            <p className="text-xs font-semibold text-slate-700">No scheduled appointments found</p>
            <p className="text-xs text-slate-400 mt-1">
              Click &quot;Generate Schedule&quot; in the top bar to run Hill Climbing optimization.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider">
                <tr>
                  <th className="py-3 px-4">Time Slot</th>
                  <th className="py-3 px-4">Patient Name</th>
                  <th className="py-3 px-4">Triage Priority</th>
                  <th className="py-3 px-4">Assigned Doctor</th>
                  <th className="py-3 px-4">Assigned Room</th>
                  <th className="py-3 px-4">Arrival Time</th>
                  <th className="py-3 px-4">Start Time</th>
                  <th className="py-3 px-4">End Time</th>
                  <th className="py-3 px-4">Waiting Time</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {filteredSchedules.map((item) => (
                  <tr key={item.id} className="hover:bg-slate-50/80 transition">
                    <td className="py-3 px-4 font-mono font-bold text-blue-700 whitespace-nowrap">
                      {item.start_time} - {item.end_time}
                    </td>
                    <td className="py-3 px-4 font-semibold text-slate-900">
                      {item.patient?.name || `Patient #${item.patient_id}`}
                    </td>
                    <td className="py-3 px-4">
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold ${
                          item.patient?.priority === 'HIGH'
                            ? 'bg-rose-100 text-rose-700 border border-rose-200'
                            : item.patient?.priority === 'MEDIUM'
                            ? 'bg-amber-100 text-amber-700 border border-amber-200'
                            : 'bg-emerald-100 text-emerald-700 border border-emerald-200'
                        }`}
                      >
                        {item.patient?.priority || 'MEDIUM'}
                      </span>
                    </td>
                    <td className="py-3 px-4 font-medium text-slate-800">
                      {item.doctor?.name || `Doctor #${item.doctor_id}`}
                    </td>
                    <td className="py-3 px-4 font-medium text-slate-800">
                      {item.room?.name || `Room #${item.room_id}`}
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-500">
                      {item.patient?.arrival_time || '--:--'}
                    </td>
                    <td className="py-3 px-4 font-mono text-slate-700">{item.start_time}</td>
                    <td className="py-3 px-4 font-mono text-slate-700">{item.end_time}</td>
                    <td className="py-3 px-4">
                      <span
                        className={`font-mono font-semibold ${
                          item.waiting_time > 20 ? 'text-amber-600 font-bold' : 'text-slate-700'
                        }`}
                      >
                        {item.waiting_time} min
                      </span>
                    </td>
                    <td className="py-3 px-4 text-right">
                      <button
                        onClick={() => setEntryToDelete(item)}
                        className="p-1.5 rounded-md hover:bg-rose-50 text-slate-400 hover:text-rose-600 transition cursor-pointer"
                        title="Cancel Appointment"
                        aria-label={`Cancel appointment for ${item.patient?.name || `Patient #${item.patient_id}`}`}
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Delete Appointment Modal */}
      <ConfirmDeleteModal
        isOpen={entryToDelete !== null}
        onClose={() => !isDeleting && setEntryToDelete(null)}
        onConfirm={handleConfirmDeleteEntry}
        title="Cancel Appointment"
        itemType="appointment"
        itemName={
          entryToDelete
            ? `${entryToDelete.patient?.name || `Patient #${entryToDelete.patient_id}`} (${entryToDelete.start_time} - ${entryToDelete.end_time})`
            : ''
        }
        warningText="Cancelling this consultation removes it from the current schedule timetable. You can re-generate the schedule at any time."
        isDeleting={isDeleting}
      />

      {/* Clear Entire Schedule Modal */}
      <ConfirmDeleteModal
        isOpen={isClearAllModalOpen}
        onClose={() => !isDeleting && setIsClearAllModalOpen(false)}
        onConfirm={handleConfirmClearAll}
        title="Clear All Schedules"
        itemType="schedule"
        itemName={`All ${schedules.length} active consultation appointments`}
        warningText="This will clear the entire generated schedule timetable. You can regenerate the timetable anytime using the Hill Climbing optimization engine."
        isDeleting={isDeleting}
      />
    </AppShell>
  );
}

