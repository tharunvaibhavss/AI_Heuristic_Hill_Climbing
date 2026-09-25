'use client';

import React, { useState, useEffect, useCallback } from 'react';
import {
  Users,
  Plus,
  Pencil,
  Trash2,
  AlertCircle,
  UserCheck,
  Search
} from 'lucide-react';
import AppShell from '@/components/AppShell';
import Modal from '@/components/Modal';
import ConfirmDeleteModal from '@/components/ConfirmDeleteModal';
import { getPatients, getDoctors, createPatient, updatePatient, deletePatient } from '@/lib/api';
import { Patient, Doctor, Priority, PatientCreate, PatientUpdate } from '@/types';

export default function PatientsPage() {
  const [patients, setPatients] = useState<Patient[]>([]);
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [loading, setLoading] = useState(true);
  const [searchQuery, setSearchQuery] = useState('');
  const [filterPriority, setFilterPriority] = useState<string>('ALL');

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingPatient, setEditingPatient] = useState<Patient | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  // Delete State
  const [patientToDelete, setPatientToDelete] = useState<Patient | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  // Form Fields
  const [formData, setFormData] = useState<{
    name: string;
    arrival_time: string;
    priority: Priority;
    consultation_duration: number;
    preferred_doctor_id: number | '';
  }>({
    name: '',
    arrival_time: '09:00',
    priority: 'MEDIUM',
    consultation_duration: 20,
    preferred_doctor_id: '',
  });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [patientsRes, doctorsRes] = await Promise.all([
        getPatients(),
        getDoctors().catch(() => [])
      ]);
      setPatients(patientsRes);
      setDoctors(doctorsRes);
    } catch (err: unknown) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleOpenAddModal = () => {
    setEditingPatient(null);
    setFormData({
      name: '',
      arrival_time: '09:15',
      priority: 'MEDIUM',
      consultation_duration: 20,
      preferred_doctor_id: '',
    });
    setFormError(null);
    setIsModalOpen(true);
  };

  const handleOpenEditModal = (p: Patient) => {
    setEditingPatient(p);
    setFormData({
      name: p.name,
      arrival_time: p.arrival_time,
      priority: p.priority,
      consultation_duration: p.consultation_duration,
      preferred_doctor_id: p.preferred_doctor_id ?? '',
    });
    setFormError(null);
    setIsModalOpen(true);
  };

  const handleFormSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    // Validation
    if (!formData.name.trim()) {
      setFormError('Patient name is required.');
      return;
    }
    const timeRegex = /^([01]\d|2[0-3]):([0-5]\d)$/;
    if (!timeRegex.test(formData.arrival_time)) {
      setFormError('Arrival time must be in HH:MM 24-hour format (e.g. 09:15).');
      return;
    }
    if (formData.consultation_duration < 10 || formData.consultation_duration > 30) {
      setFormError('Consultation duration must be between 10 and 30 minutes.');
      return;
    }

    try {
      setSaving(true);
      const payload: PatientCreate | PatientUpdate = {
        name: formData.name.trim(),
        arrival_time: formData.arrival_time,
        priority: formData.priority,
        consultation_duration: Number(formData.consultation_duration),
        preferred_doctor_id: formData.preferred_doctor_id === '' ? null : Number(formData.preferred_doctor_id),
      };

      if (editingPatient) {
        await updatePatient(editingPatient.id, payload);
        setNotification({
          type: 'success',
          message: `Patient "${formData.name.trim()}" updated successfully.`,
        });
      } else {
        await createPatient(payload as PatientCreate);
        setNotification({
          type: 'success',
          message: `Patient "${formData.name.trim()}" registered successfully.`,
        });
      }

      setIsModalOpen(false);
      await loadData();
    } catch (err: unknown) {
      setFormError(err instanceof Error ? err.message : 'Operation failed.');
    } finally {
      setSaving(false);
    }
  };

  const handleConfirmDelete = async () => {
    if (!patientToDelete) return;
    try {
      setIsDeleting(true);
      await deletePatient(patientToDelete.id);
      setNotification({
        type: 'success',
        message: `Patient "${patientToDelete.name}" was successfully removed.`,
      });
      setPatientToDelete(null);
      await loadData();
    } catch (err: unknown) {
      setNotification({
        type: 'error',
        message: err instanceof Error ? err.message : 'Failed to delete patient',
      });
      setPatientToDelete(null);
    } finally {
      setIsDeleting(false);
    }
  };


  const filteredPatients = patients.filter((p) => {
    const matchesSearch = p.name.toLowerCase().includes(searchQuery.toLowerCase());
    const matchesPriority = filterPriority === 'ALL' || p.priority === filterPriority;
    return matchesSearch && matchesPriority;
  });

  return (
    <AppShell
      title="Patient Management"
      subtitle="Register, update triage priorities, and configure consultation preferences"
      onDataRefresh={loadData}
    >
      {/* Top Filter and Action Bar */}
      <div className="flex flex-col sm:flex-row items-stretch sm:items-center justify-between gap-3 bg-white p-4 rounded-xl border border-slate-200 shadow-2xs">
        <div className="flex items-center gap-3 flex-1 flex-wrap">
          {/* Search */}
          <div className="relative flex-1 min-w-[200px]">
            <Search className="h-4 w-4 absolute left-3 top-1/2 -translate-y-1/2 text-slate-400" />
            <input
              type="text"
              placeholder="Search patients by name..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              className="w-full pl-9 pr-3 py-1.5 text-xs rounded-lg border border-slate-200 focus:outline-hidden focus:border-blue-500 transition"
            />
          </div>

          {/* Priority Filter */}
          <div className="flex items-center gap-1">
            <span className="text-xs text-slate-500 font-medium">Priority:</span>
            <select
              value={filterPriority}
              onChange={(e) => setFilterPriority(e.target.value)}
              className="text-xs py-1.5 px-2.5 rounded-lg border border-slate-200 bg-white focus:outline-hidden focus:border-blue-500"
            >
              <option value="ALL">All Priorities</option>
              <option value="HIGH">HIGH Priority</option>
              <option value="MEDIUM">MEDIUM Priority</option>
              <option value="LOW">LOW Priority</option>
            </select>
          </div>
        </div>

        {/* Add Patient Button */}
        <button
          onClick={handleOpenAddModal}
          className="inline-flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-xs transition cursor-pointer shrink-0"
        >
          <Plus className="h-4 w-4" />
          Add Patient
        </button>
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
              <UserCheck className="h-4 w-4 text-emerald-600 shrink-0" />
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

      {/* Patients Table Card */}

      <div className="bg-white rounded-xl border border-slate-200 shadow-2xs overflow-hidden">
        <div className="px-6 py-3.5 border-b border-slate-100 flex items-center justify-between">
          <span className="text-xs font-bold text-slate-700 uppercase tracking-wider">
            Patient Roster ({filteredPatients.length} of {patients.length})
          </span>
          <span className="text-xs text-slate-400">
            Click edit to update triage or doctor preferences
          </span>
        </div>

        {loading ? (
          <div className="p-12 text-center text-xs text-slate-400">Loading patients from database...</div>
        ) : filteredPatients.length === 0 ? (
          <div className="p-12 text-center text-slate-500">
            <Users className="h-8 w-8 text-slate-300 mx-auto mb-2" />
            <p className="text-xs font-semibold text-slate-700">No patients found</p>
            <p className="text-xs text-slate-400 mt-1">
              Try adjusting your search criteria or click &quot;Add Patient&quot; above.
            </p>
          </div>
        ) : (
          <div className="overflow-x-auto">
            <table className="w-full text-left text-xs">
              <thead className="bg-slate-50 border-b border-slate-200 text-slate-600 font-semibold uppercase tracking-wider">
                <tr>
                  <th className="py-3 px-4">ID</th>
                  <th className="py-3 px-4">Patient Name</th>
                  <th className="py-3 px-4">Arrival Time</th>
                  <th className="py-3 px-4">Priority Level</th>
                  <th className="py-3 px-4">Expected Duration</th>
                  <th className="py-3 px-4">Preferred Doctor</th>
                  <th className="py-3 px-4 text-right">Actions</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-100 text-slate-700">
                {filteredPatients.map((p) => (
                  <tr key={p.id} className="hover:bg-slate-50/80 transition">
                    <td className="py-3 px-4 font-mono font-medium text-slate-400">#{p.id}</td>
                    <td className="py-3 px-4 font-semibold text-slate-900">{p.name}</td>
                    <td className="py-3 px-4 font-mono font-medium">{p.arrival_time}</td>
                    <td className="py-3 px-4">
                      <span
                        className={`inline-flex items-center px-2 py-0.5 rounded text-[11px] font-bold ${
                          p.priority === 'HIGH'
                            ? 'bg-rose-100 text-rose-700 border border-rose-200'
                            : p.priority === 'MEDIUM'
                            ? 'bg-amber-100 text-amber-700 border border-amber-200'
                            : 'bg-emerald-100 text-emerald-700 border border-emerald-200'
                        }`}
                      >
                        {p.priority}
                      </span>
                    </td>
                    <td className="py-3 px-4">
                      <span className="font-medium text-slate-800">{p.consultation_duration} min</span>
                    </td>
                    <td className="py-3 px-4">
                      {p.preferred_doctor ? (
                        <span className="inline-flex items-center gap-1 text-slate-800 font-medium">
                          <UserCheck className="h-3.5 w-3.5 text-blue-600" />
                          {p.preferred_doctor.name}
                        </span>
                      ) : (
                        <span className="text-slate-400 italic">No preference</span>
                      )}
                    </td>
                    <td className="py-3 px-4 text-right">
                      <div className="inline-flex items-center gap-1">
                        <button
                          onClick={() => handleOpenEditModal(p)}
                          className="p-1.5 rounded-md hover:bg-slate-100 text-slate-600 hover:text-blue-600 transition"
                          title="Edit Patient"
                        >
                          <Pencil className="h-3.5 w-3.5" />
                        </button>
                        <button
                          onClick={() => setPatientToDelete(p)}
                          className="p-1.5 rounded-md hover:bg-rose-50 text-slate-400 hover:text-rose-600 transition cursor-pointer"
                          title="Delete Patient"
                          aria-label={`Delete patient ${p.name}`}
                        >
                          <Trash2 className="h-3.5 w-3.5" />
                        </button>
                      </div>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>

      {/* Add / Edit Patient Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingPatient ? `Edit Patient: ${editingPatient.name}` : 'Register New Patient'}
      >
        <form onSubmit={handleFormSubmit} className="space-y-4">
          {formError && (
            <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>{formError}</span>
            </div>
          )}

          {/* Name */}
          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g. John Doe"
              className="w-full text-xs py-2 px-3 rounded-lg border border-slate-300 focus:outline-hidden focus:border-blue-500"
            />
          </div>

          {/* Arrival Time & Priority */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Arrival Time (HH:MM)
              </label>
              <input
                type="text"
                required
                value={formData.arrival_time}
                onChange={(e) => setFormData({ ...formData, arrival_time: e.target.value })}
                placeholder="09:15"
                className="w-full text-xs py-2 px-3 rounded-lg border border-slate-300 font-mono focus:outline-hidden focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">Triage Priority</label>
              <select
                value={formData.priority}
                onChange={(e) => setFormData({ ...formData, priority: e.target.value as Priority })}
                className="w-full text-xs py-2 px-3 rounded-lg border border-slate-300 bg-white focus:outline-hidden focus:border-blue-500"
              >
                <option value="HIGH">HIGH (Acute / Emergency)</option>
                <option value="MEDIUM">MEDIUM (Standard Urgent)</option>
                <option value="LOW">LOW (Routine / Wellness)</option>
              </select>
            </div>
          </div>

          {/* Duration & Preferred Doctor */}
          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Duration (10–30 mins)
              </label>
              <input
                type="number"
                min={10}
                max={30}
                required
                value={formData.consultation_duration}
                onChange={(e) => setFormData({ ...formData, consultation_duration: Number(e.target.value) })}
                className="w-full text-xs py-2 px-3 rounded-lg border border-slate-300 focus:outline-hidden focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Preferred Doctor
              </label>
              <select
                value={formData.preferred_doctor_id}
                onChange={(e) =>
                  setFormData({
                    ...formData,
                    preferred_doctor_id: e.target.value === '' ? '' : Number(e.target.value),
                  })
                }
                className="w-full text-xs py-2 px-3 rounded-lg border border-slate-300 bg-white focus:outline-hidden focus:border-blue-500"
              >
                <option value="">No Preference</option>
                {doctors.map((d) => (
                  <option key={d.id} value={d.id}>
                    {d.name}
                  </option>
                ))}
              </select>
            </div>
          </div>

          {/* Action Buttons */}
          <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
            {editingPatient ? (
              <button
                type="button"
                onClick={() => {
                  const toDelete = editingPatient;
                  setIsModalOpen(false);
                  setPatientToDelete(toDelete);
                }}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-rose-600 hover:text-rose-700 hover:bg-rose-50 border border-rose-200 text-xs font-semibold transition cursor-pointer"
              >
                <Trash2 className="h-3.5 w-3.5" />
                <span>Delete Patient</span>
              </button>
            ) : (
              <div />
            )}
            <div className="flex items-center gap-2">
              <button
                type="button"
                onClick={() => setIsModalOpen(false)}
                className="px-3.5 py-1.5 rounded-lg border border-slate-300 text-xs font-medium text-slate-700 hover:bg-slate-50 transition cursor-pointer"
              >
                Cancel
              </button>
              <button
                type="submit"
                disabled={saving}
                className="px-4 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold transition disabled:opacity-60 cursor-pointer"
              >
                {saving ? 'Saving...' : editingPatient ? 'Update Patient' : 'Save Patient'}
              </button>
            </div>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation Modal */}
      <ConfirmDeleteModal
        isOpen={patientToDelete !== null}
        onClose={() => !isDeleting && setPatientToDelete(null)}
        onConfirm={handleConfirmDelete}
        title="Delete Patient"
        itemType="patient"
        itemName={patientToDelete?.name || ''}
        warningText="Permanently removing this patient will immediately unassign and cancel any consultation schedules linked to them in the hospital database."
        isDeleting={isDeleting}
      />
    </AppShell>
  );
}

