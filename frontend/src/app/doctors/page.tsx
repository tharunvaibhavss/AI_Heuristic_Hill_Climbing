'use client';

import React, { useState, useEffect, useCallback } from 'react';
import {
  Stethoscope,
  Plus,
  Pencil,
  Trash2,
  Clock,
  AlertCircle
} from 'lucide-react';
import AppShell from '@/components/AppShell';
import Modal from '@/components/Modal';
import ConfirmDeleteModal from '@/components/ConfirmDeleteModal';
import { getDoctors, getSchedule, createDoctor, updateDoctor, deleteDoctor } from '@/lib/api';
import { Doctor, DoctorCreate, DoctorUpdate, Schedule } from '@/types';


export default function DoctorsPage() {
  const [doctors, setDoctors] = useState<Doctor[]>([]);
  const [schedules, setSchedules] = useState<Schedule[]>([]);
  const [loading, setLoading] = useState(true);

  // Modal State
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [editingDoctor, setEditingDoctor] = useState<Doctor | null>(null);
  const [formError, setFormError] = useState<string | null>(null);
  const [saving, setSaving] = useState(false);

  // Delete State
  const [docToDelete, setDocToDelete] = useState<Doctor | null>(null);
  const [isDeleting, setIsDeleting] = useState(false);
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  // Form Fields
  const [formData, setFormData] = useState<DoctorCreate>({
    name: '',
    available_from: '09:00',
    available_until: '13:00',
  });

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const [docsRes, schedRes] = await Promise.all([
        getDoctors(),
        getSchedule().catch(() => [])
      ]);
      setDoctors(docsRes);
      setSchedules(schedRes);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const handleOpenAdd = () => {
    setEditingDoctor(null);
    setFormData({
      name: '',
      available_from: '09:00',
      available_until: '13:00',
    });
    setFormError(null);
    setIsModalOpen(true);
  };

  const handleOpenEdit = (doc: Doctor) => {
    setEditingDoctor(doc);
    setFormData({
      name: doc.name,
      available_from: doc.available_from,
      available_until: doc.available_until,
    });
    setFormError(null);
    setIsModalOpen(true);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setFormError(null);

    if (!formData.name.trim()) {
      setFormError('Doctor name is required.');
      return;
    }
    const timeRegex = /^([01]\d|2[0-3]):([0-5]\d)$/;
    if (!timeRegex.test(formData.available_from) || !timeRegex.test(formData.available_until)) {
      setFormError('Hours must be in valid 24h format (e.g. 09:00).');
      return;
    }

    try {
      setSaving(true);
      if (editingDoctor) {
        await updateDoctor(editingDoctor.id, formData as DoctorUpdate);
        setNotification({
          type: 'success',
          message: `Doctor "${formData.name.trim()}" updated successfully.`,
        });
      } else {
        await createDoctor(formData);
        setNotification({
          type: 'success',
          message: `Doctor "${formData.name.trim()}" added to staff roster.`,
        });
      }
      setIsModalOpen(false);
      await loadData();
    } catch (err: unknown) {
      setFormError(err instanceof Error ? err.message : 'Operation failed');
    } finally {
      setSaving(false);
    }
  };

  const handleConfirmDelete = async () => {
    if (!docToDelete) return;
    try {
      setIsDeleting(true);
      await deleteDoctor(docToDelete.id);
      setNotification({
        type: 'success',
        message: `Doctor "${docToDelete.name}" was removed from the roster.`,
      });
      setDocToDelete(null);
      await loadData();
    } catch (err: unknown) {
      setNotification({
        type: 'error',
        message: err instanceof Error ? err.message : 'Failed to delete doctor',
      });
      setDocToDelete(null);
    } finally {
      setIsDeleting(false);
    }
  };


  // Compute doctor workload & utilization
  const getDoctorStats = (docId: number) => {
    const assignedAppts = schedules.filter((s) => s.doctor_id === docId);
    let usedMinutes = 0;
    for (const appt of assignedAppts) {
      // Calculate minutes
      const [sh, sm] = appt.start_time.split(':').map(Number);
      const [eh, em] = appt.end_time.split(':').map(Number);
      usedMinutes += (eh * 60 + em) - (sh * 60 + sm);
    }
    const totalCapacity = 240; // 4 hours from 09:00 to 13:00
    const utilizationRate = Math.min(100, Math.round((usedMinutes / totalCapacity) * 100));

    return {
      assignedCount: assignedAppts.length,
      usedMinutes,
      utilizationRate,
    };
  };

  return (
    <AppShell
      title="Doctor Management"
      subtitle="Configure clinical staff, operating shifts, and review consultation workloads"
      onDataRefresh={loadData}
    >
      {/* Action Header */}
      <div className="flex items-center justify-between bg-white p-4 rounded-xl border border-slate-200 shadow-2xs">
        <div>
          <h2 className="text-sm font-bold text-slate-800">Medical Staff Roster</h2>
          <p className="text-xs text-slate-500">
            {doctors.length} doctors registered with active availability
          </p>
        </div>
        <button
          onClick={handleOpenAdd}
          className="inline-flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold shadow-xs transition cursor-pointer"
        >
          <Plus className="h-4 w-4" />
          Add Doctor
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
              <Stethoscope className="h-4 w-4 text-emerald-600 shrink-0" />
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

      {/* Doctors Grid */}
      {loading ? (
        <div className="p-12 text-center text-xs text-slate-400">Loading doctor profiles...</div>
      ) : doctors.length === 0 ? (
        <div className="p-12 text-center text-slate-500 bg-white rounded-xl border border-slate-200">
          <Stethoscope className="h-8 w-8 text-slate-300 mx-auto mb-2" />
          <p className="text-xs font-semibold text-slate-700">No doctors found</p>
          <p className="text-xs text-slate-400 mt-1">Click &quot;Add Doctor&quot; to register medical staff.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {doctors.map((doc) => {
            const stats = getDoctorStats(doc.id);
            return (
              <div
                key={doc.id}
                className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs hover:border-slate-300 transition flex flex-col justify-between"
              >
                <div>
                  <div className="flex items-start justify-between">
                    <div className="h-10 w-10 rounded-xl bg-indigo-50 text-indigo-700 flex items-center justify-center font-bold text-sm">
                      MD
                    </div>
                    <div className="flex items-center gap-1">
                      <button
                        onClick={() => handleOpenEdit(doc)}
                        className="p-1.5 rounded-md text-slate-400 hover:text-blue-600 hover:bg-slate-50 transition"
                        title="Edit Doctor"
                      >
                        <Pencil className="h-3.5 w-3.5" />
                      </button>
                      <button
                        onClick={() => setDocToDelete(doc)}
                        className="p-1.5 rounded-md text-slate-400 hover:text-rose-600 hover:bg-rose-50 transition cursor-pointer"
                        title="Delete Doctor"
                        aria-label={`Delete doctor ${doc.name}`}
                      >
                        <Trash2 className="h-3.5 w-3.5" />
                      </button>
                    </div>
                  </div>

                  <h3 className="text-sm font-bold text-slate-900 mt-3">{doc.name}</h3>
                  <div className="mt-1 flex items-center gap-1 text-xs text-slate-500">
                    <Clock className="h-3.5 w-3.5 text-slate-400" />
                    <span>{doc.available_from} - {doc.available_until}</span>
                  </div>
                </div>

                <div className="mt-4 pt-4 border-t border-slate-100 space-y-2">
                  <div className="flex items-center justify-between text-xs">
                    <span className="text-slate-500 font-medium">Assigned Patients:</span>
                    <span className="font-bold text-slate-900">{stats.assignedCount}</span>
                  </div>

                  <div>
                    <div className="flex items-center justify-between text-xs mb-1">
                      <span className="text-slate-500 font-medium">Utilization:</span>
                      <span className="font-mono font-semibold text-indigo-600">
                        {stats.utilizationRate}% ({stats.usedMinutes}m / 240m)
                      </span>
                    </div>
                    <div className="w-full bg-slate-100 rounded-full h-1.5 overflow-hidden">
                      <div
                        className="bg-indigo-600 h-1.5 rounded-full transition-all duration-300"
                        style={{ width: `${stats.utilizationRate}%` }}
                      />
                    </div>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      {/* Add / Edit Doctor Modal */}
      <Modal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        title={editingDoctor ? `Edit Doctor: ${editingDoctor.name}` : 'Register New Doctor'}
      >
        <form onSubmit={handleSubmit} className="space-y-4">
          {formError && (
            <div className="p-3 rounded-lg bg-rose-50 border border-rose-200 text-rose-700 text-xs flex items-center gap-2">
              <AlertCircle className="h-4 w-4 shrink-0" />
              <span>{formError}</span>
            </div>
          )}

          <div>
            <label className="block text-xs font-semibold text-slate-700 mb-1">Full Name</label>
            <input
              type="text"
              required
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              placeholder="e.g. Dr. John Watson"
              className="w-full text-xs py-2 px-3 rounded-lg border border-slate-300 focus:outline-hidden focus:border-blue-500"
            />
          </div>

          <div className="grid grid-cols-2 gap-3">
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Available From (HH:MM)
              </label>
              <input
                type="text"
                required
                value={formData.available_from}
                onChange={(e) => setFormData({ ...formData, available_from: e.target.value })}
                placeholder="09:00"
                className="w-full text-xs py-2 px-3 rounded-lg border border-slate-300 font-mono focus:outline-hidden focus:border-blue-500"
              />
            </div>
            <div>
              <label className="block text-xs font-semibold text-slate-700 mb-1">
                Available Until (HH:MM)
              </label>
              <input
                type="text"
                required
                value={formData.available_until}
                onChange={(e) => setFormData({ ...formData, available_until: e.target.value })}
                placeholder="13:00"
                className="w-full text-xs py-2 px-3 rounded-lg border border-slate-300 font-mono focus:outline-hidden focus:border-blue-500"
              />
            </div>
          </div>

          <div className="pt-3 border-t border-slate-100 flex items-center justify-between gap-2">
            {editingDoctor ? (
              <button
                type="button"
                onClick={() => {
                  const toDelete = editingDoctor;
                  setIsModalOpen(false);
                  setDocToDelete(toDelete);
                }}
                className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-rose-600 hover:text-rose-700 hover:bg-rose-50 border border-rose-200 text-xs font-semibold transition cursor-pointer"
              >
                <Trash2 className="h-3.5 w-3.5" />
                <span>Delete Doctor</span>
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
                {saving ? 'Saving...' : editingDoctor ? 'Update Doctor' : 'Save Doctor'}
              </button>
            </div>
          </div>
        </form>
      </Modal>

      {/* Delete Confirmation Modal */}
      <ConfirmDeleteModal
        isOpen={docToDelete !== null}
        onClose={() => !isDeleting && setDocToDelete(null)}
        onConfirm={handleConfirmDelete}
        title="Delete Doctor"
        itemType="doctor"
        itemName={docToDelete?.name || ''}
        warningText="Permanently removing this doctor will unassign them from any patient preference and cancel any scheduled consultations assigned to them."
        isDeleting={isDeleting}
      />
    </AppShell>
  );
}

