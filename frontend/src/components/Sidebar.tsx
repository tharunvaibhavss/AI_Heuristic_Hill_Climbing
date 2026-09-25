'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  LayoutDashboard,
  Users,
  Stethoscope,
  Building2,
  CalendarDays,
  BrainCircuit,
  Activity,
  X
} from 'lucide-react';

interface SidebarProps {
  isOpen: boolean;
  onClose: () => void;
}

const NAV_ITEMS = [
  { href: '/', label: 'Dashboard', icon: LayoutDashboard },
  { href: '/patients', label: 'Patients', icon: Users },
  { href: '/doctors', label: 'Doctors', icon: Stethoscope },
  { href: '/rooms', label: 'Rooms', icon: Building2 },
  { href: '/schedule', label: 'Schedule', icon: CalendarDays },
  { href: '/heuristic', label: 'Heuristic Analysis', icon: BrainCircuit },
];

export default function Sidebar({ isOpen, onClose }: SidebarProps) {
  const pathname = usePathname();

  return (
    <>
      {/* Mobile Backdrop */}
      {isOpen && (
        <div
          onClick={onClose}
          className="fixed inset-0 bg-slate-900/50 backdrop-blur-xs z-40 lg:hidden"
        />
      )}

      {/* Sidebar Container */}
      <aside
        className={`fixed top-0 bottom-0 left-0 z-50 w-64 bg-slate-900 text-slate-100 flex flex-col transition-transform duration-200 ease-in-out lg:translate-x-0 ${
          isOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        {/* Brand Header */}
        <div className="h-16 px-5 border-b border-slate-800 flex items-center justify-between">
          <Link href="/" className="flex items-center gap-3" onClick={onClose}>
            <div className="h-9 w-9 rounded-lg bg-blue-600 flex items-center justify-center text-white shadow-md shadow-blue-500/20">
              <Activity className="h-5 w-5" />
            </div>
            <div>
              <div className="text-sm font-bold tracking-tight text-white leading-tight">
                MedSchedule AI
              </div>
              <div className="text-[10px] text-blue-400 font-medium">
                Hill Climbing Engine
              </div>
            </div>
          </Link>
          <button
            onClick={onClose}
            className="lg:hidden p-1.5 rounded-lg text-slate-400 hover:text-white hover:bg-slate-800 transition"
          >
            <X className="h-5 w-5" />
          </button>
        </div>

        {/* Navigation Links */}
        <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
          <div className="px-3 pb-2 text-[10px] font-bold uppercase tracking-wider text-slate-400">
            Navigation
          </div>
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                onClick={onClose}
                className={`flex items-center gap-3 px-3 py-2.5 rounded-lg text-xs font-semibold transition ${
                  isActive
                    ? 'bg-blue-600 text-white shadow-sm shadow-blue-600/30'
                    : 'text-slate-300 hover:text-white hover:bg-slate-800/80'
                }`}
              >
                <Icon className={`h-4 w-4 shrink-0 ${isActive ? 'text-white' : 'text-slate-400'}`} />
                {item.label}
              </Link>
            );
          })}
        </nav>

        {/* Algorithm Formulation Badge */}
        <div className="p-3 m-3 rounded-xl bg-slate-800/80 border border-slate-700/60 text-xs">
          <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">
            Objective Function
          </div>
          <div className="font-mono text-[11px] text-blue-300 font-semibold mt-1">
            H(S) = 5(WT) + 100(C) + 20(P) + 10(U)
          </div>
          <div className="text-[10px] text-slate-400 mt-1">
            Minimization via Best-Improvement Hill Climbing
          </div>
        </div>
      </aside>
    </>
  );
}
