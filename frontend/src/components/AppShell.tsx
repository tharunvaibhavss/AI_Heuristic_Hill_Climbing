'use client';

import React, { useState, useEffect } from 'react';
import { Menu, RefreshCw, Play, CheckCircle2, AlertCircle } from 'lucide-react';
import Sidebar from '@/components/Sidebar';
import { getHealth, generateSchedule, resetDatabase } from '@/lib/api';
import { BackendHealth } from '@/types';

interface AppShellProps {
  children: React.ReactNode;
  title: string;
  subtitle?: string;
  onDataRefresh?: () => void;
}

export default function AppShell({ children, title, subtitle, onDataRefresh }: AppShellProps) {
  const [sidebarOpen, setSidebarOpen] = useState(false);
  const [health, setHealth] = useState<BackendHealth | null>(null);
  const [generating, setGenerating] = useState(false);
  const [resetting, setResetting] = useState(false);
  const [notification, setNotification] = useState<{ type: 'success' | 'error'; message: string } | null>(null);

  const checkHealth = async () => {
    try {
      const h = await getHealth();
      setHealth(h);
    } catch {
      setHealth(null);
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000); // 30s heartbeat
    return () => clearInterval(interval);
  }, []);

  const handleGenerate = async () => {
    try {
      setGenerating(true);
      setNotification(null);
      const res = await generateSchedule();
      setNotification({
        type: 'success',
        message: `Schedule generated! Initial H(S)=${res.initial_score}, Final H(S)=${res.final_score} (${res.iterations} iterations, -${res.improvement} improvement)`,
      });
      checkHealth();
      if (onDataRefresh) {
        onDataRefresh();
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to generate schedule';
      setNotification({
        type: 'error',
        message: `Optimization error: ${msg}. Make sure FastAPI is running.`,
      });
    } finally {
      setGenerating(false);
    }
  };

  const handleReset = async () => {
    if (!confirm('Are you sure you want to reset the database to the 20-patient seed dataset?')) {
      return;
    }
    try {
      setResetting(true);
      setNotification(null);
      await resetDatabase();
      setNotification({
        type: 'success',
        message: 'Database reset and re-seeded successfully with 20 patients, 4 doctors, and 3 rooms.',
      });
      checkHealth();
      if (onDataRefresh) {
        onDataRefresh();
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Failed to reset database';
      setNotification({
        type: 'error',
        message: `Reset failed: ${msg}`,
      });
    } finally {
      setResetting(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-50 flex">
      {/* Sidebar */}
      <Sidebar isOpen={sidebarOpen} onClose={() => setSidebarOpen(false)} />

      {/* Main Content Area */}
      <div className="flex-1 flex flex-col min-w-0 lg:pl-64">
        {/* Top Navbar */}
        <header className="h-16 bg-white border-b border-slate-200 sticky top-0 z-30 flex items-center justify-between px-4 sm:px-6 lg:px-8 shadow-2xs">
          <div className="flex items-center gap-3">
            <button
              onClick={() => setSidebarOpen(true)}
              className="lg:hidden p-2 rounded-lg text-slate-600 hover:text-slate-900 hover:bg-slate-100 transition"
              aria-label="Open sidebar"
            >
              <Menu className="h-5 w-5" />
            </button>
            <div>
              <h1 className="text-base font-bold text-slate-900 leading-tight">{title}</h1>
              {subtitle && <p className="text-xs text-slate-500 hidden sm:block">{subtitle}</p>}
            </div>
          </div>

          {/* Actions & Health Badge */}
          <div className="flex items-center gap-2.5">
            {health ? (
              <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-700 text-xs font-semibold">
                <span className="h-2 w-2 rounded-full bg-emerald-500 animate-pulse" />
                Backend Connected
              </div>
            ) : (
              <div className="hidden sm:flex items-center gap-1.5 px-2.5 py-1 rounded-full bg-rose-50 border border-rose-200 text-rose-700 text-xs font-semibold">
                <span className="h-2 w-2 rounded-full bg-rose-500" />
                Backend Offline
              </div>
            )}

            <button
              onClick={handleGenerate}
              disabled={generating}
              className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold transition shadow-xs disabled:opacity-60 cursor-pointer"
            >
              {generating ? (
                <>
                  <RefreshCw className="h-3.5 w-3.5 animate-spin" />
                  <span>Optimizing Schedule...</span>
                </>
              ) : (
                <>
                  <Play className="h-3.5 w-3.5 fill-current" />
                  <span>Generate Schedule</span>
                </>
              )}
            </button>

            <button
              onClick={handleReset}
              disabled={resetting}
              className="inline-flex items-center gap-1.5 px-2.5 py-1.5 rounded-lg border border-slate-200 bg-white hover:bg-slate-50 text-slate-700 text-xs font-medium transition shadow-2xs disabled:opacity-60 cursor-pointer"
              title="Reset & Re-seed DB"
            >
              <RefreshCw className={`h-3.5 w-3.5 ${resetting ? 'animate-spin text-blue-600' : ''}`} />
              <span className="hidden md:inline">Reset DB</span>
            </button>
          </div>
        </header>

        {/* Global Notification Banner */}
        {notification && (
          <div
            className={`mx-4 sm:mx-6 lg:mx-8 mt-4 p-3.5 rounded-xl border flex items-start justify-between text-xs font-medium transition ${
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
              className="ml-4 font-bold hover:underline shrink-0"
            >
              Dismiss
            </button>
          </div>
        )}

        {/* Page Content */}
        <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl w-full mx-auto space-y-6">
          {children}
        </main>

        {/* Footer */}
        <footer className="border-t border-slate-200 bg-white py-3.5 px-4 text-center text-xs text-slate-500">
          Hospital Patient Scheduling using Heuristic Function &amp; Hill Climbing &bull; Academic AI Project
        </footer>
      </div>
    </div>
  );
}
