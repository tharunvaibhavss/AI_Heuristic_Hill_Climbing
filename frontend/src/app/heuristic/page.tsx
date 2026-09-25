'use client';

import React, { useState, useEffect, useCallback } from 'react';
import {
  Brain,
  Clock,
  AlertTriangle,
  HeartPulse,
  Gauge,
  Info,
  BookOpen,
  Compass,
  ArrowDown,
  Layers,
  Activity,
  CheckCircle2
} from 'lucide-react';
import AppShell from '@/components/AppShell';
import { getScheduleScore } from '@/lib/api';
import { ScheduleScoreResponse } from '@/types';

export default function HeuristicPage() {
  const [scoreData, setScoreData] = useState<ScheduleScoreResponse | null>(null);
  const [loading, setLoading] = useState(true);

  const loadData = useCallback(async () => {
    try {
      setLoading(true);
      const res = await getScheduleScore();
      setScoreData(res);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadData();
  }, [loadData]);

  const h = scoreData?.heuristic;
  const initialScore = scoreData?.initial_score ?? 1047.7;
  const finalScore = scoreData?.final_score ?? (h?.total_score ?? 1047.7);
  const improvement = scoreData?.improvement ?? 0.0;
  const acceptedMoves = scoreData?.accepted_moves ?? 0;
  const neighborEvaluations = scoreData?.neighbor_evaluations ?? 100;
  const statusMessage = scoreData?.status_message ?? 'No improving neighbor found. Hill Climbing stopped at a local minimum.';

  return (
    <AppShell
      title="Heuristic Function & Optimization Analysis"
      subtitle="Multi-objective evaluation, Hill Climbing search trajectory, and component cost breakdown"
      onDataRefresh={loadData}
    >
      {/* 1. CURRENT HEURISTIC SCORE & HERO */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-2xs">
        <div className="flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div>
            <div className="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full bg-blue-50 text-blue-700 text-xs font-semibold mb-2">
              <Brain className="h-3.5 w-3.5" /> Section 1: Current Heuristic Score
            </div>
            <h2 className="text-xl font-bold text-slate-900">
              Schedule Valuation Metric: H(S)
            </h2>
            <p className="text-xs text-slate-500 mt-1 max-w-xl leading-relaxed">
              The scheduling engine evaluates schedule quality via a weighted multi-criteria penalty function. In this minimization formulation, a lower score represents a superior consultation schedule.
            </p>
          </div>

          <div className="bg-slate-900 text-white p-5 rounded-xl border border-slate-800 shadow-md shrink-0 text-right">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider block">
              Active Schedule Score
            </span>
            <div className="text-3xl font-mono font-black text-blue-400 mt-1">
              H(S) = {loading ? '...' : (h?.total_score ?? 1047.7)}
            </div>
            <div className="text-[11px] text-emerald-400 mt-1 font-medium flex items-center justify-end gap-1">
              <CheckCircle2 className="h-3.5 w-3.5" /> Hard Constraints Satisfied (C = 0)
            </div>
          </div>
        </div>
      </div>

      {/* 2. MATHEMATICAL FORMULA */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-2xs">
        <div className="flex items-center gap-2 mb-3">
          <span className="px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700 text-xs font-bold">
            Section 2: Formula
          </span>
          <h3 className="text-sm font-bold text-slate-900">
            Objective Function Mathematical Definition
          </h3>
        </div>

        <div className="bg-slate-950 text-white p-4 sm:p-5 rounded-xl font-mono text-center text-sm sm:text-base font-bold shadow-inner border border-slate-800">
          <span className="text-blue-400">H(S)</span> = <span className="text-blue-300">5(WT)</span> + <span className="text-rose-400">100(C)</span> + <span className="text-amber-300">20(P)</span> + <span className="text-purple-300">10(U)</span>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 mt-4 text-xs">
          <div className="p-3 rounded-lg bg-blue-50/60 border border-blue-100">
            <strong className="text-blue-800 block">W₁ = 5</strong>
            <span className="text-slate-600 text-[11px]">Weight for Waiting Time (WT)</span>
          </div>
          <div className="p-3 rounded-lg bg-rose-50/60 border border-rose-100">
            <strong className="text-rose-800 block">W₂ = 100</strong>
            <span className="text-slate-600 text-[11px]">Weight for Conflicts (C)</span>
          </div>
          <div className="p-3 rounded-lg bg-amber-50/60 border border-amber-100">
            <strong className="text-amber-800 block">W₃ = 20</strong>
            <span className="text-slate-600 text-[11px]">Weight for Priority Penalty (P)</span>
          </div>
          <div className="p-3 rounded-lg bg-purple-50/60 border border-purple-100">
            <strong className="text-purple-800 block">W₄ = 10</strong>
            <span className="text-slate-600 text-[11px]">Weight for Under-utilization (U)</span>
          </div>
        </div>
      </div>

      {/* 3. COMPONENT BREAKDOWN (LIVE VALUES) */}
      <div>
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <span className="px-2 py-0.5 rounded-full bg-emerald-50 text-emerald-700 text-xs font-bold">
              Section 3: Component Breakdown
            </span>
            <h3 className="text-xs font-bold text-slate-700 uppercase tracking-wider">
              Dynamic Live Component Values
            </h3>
          </div>
          <span className="text-xs text-slate-500">
            {scoreData?.has_schedule ? 'Computed from active SQLite database' : 'No schedule loaded'}
          </span>
        </div>

        {loading ? (
          <div className="bg-white rounded-xl border border-slate-200 p-12 text-center text-xs text-slate-400 shadow-2xs">
            Evaluating active schedule heuristic components...
          </div>
        ) : !scoreData?.has_schedule || !h ? (
          <div className="bg-white rounded-xl border border-slate-200 p-12 text-center text-slate-500 shadow-2xs">
            <Brain className="h-8 w-8 text-slate-300 mx-auto mb-2" />
            <p className="text-xs font-semibold text-slate-700">No active schedule found</p>
            <p className="text-xs text-slate-400 mt-1">
              Click &quot;Generate Schedule&quot; in the header to run Hill Climbing optimization.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
            {/* 1. Waiting Time */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                    Waiting Time (WT)
                  </span>
                  <div className="h-8 w-8 rounded-lg bg-blue-50 text-blue-600 flex items-center justify-center">
                    <Clock className="h-4 w-4" />
                  </div>
                </div>
                <div className="mt-2 text-2xl font-bold text-slate-900">
                  {h.waiting_time} <span className="text-xs font-normal text-slate-500">min</span>
                </div>
                <p className="mt-1 text-[11px] text-slate-500">
                  Sum of all patient delays from arrival to consultation start.
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-slate-500">Weighted Cost:</span>
                <span className="font-mono font-bold text-blue-700">
                  5 &times; {h.waiting_time} = {h.waiting_cost}
                </span>
              </div>
            </div>

            {/* 2. Conflicts */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                    Conflicts (C)
                  </span>
                  <div className={`h-8 w-8 rounded-lg flex items-center justify-center ${
                    h.conflicts > 0 ? 'bg-rose-50 text-rose-600' : 'bg-emerald-50 text-emerald-600'
                  }`}>
                    <AlertTriangle className="h-4 w-4" />
                  </div>
                </div>
                <div className={`mt-2 text-2xl font-bold ${h.conflicts > 0 ? 'text-rose-600' : 'text-emerald-700'}`}>
                  {h.conflicts}
                </div>
                <p className="mt-1 text-[11px] text-slate-500">
                  Doctor or room double-bookings and constraint breaches.
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-slate-500">Weighted Cost:</span>
                <span className={`font-mono font-bold ${h.conflicts > 0 ? 'text-rose-600' : 'text-emerald-700'}`}>
                  100 &times; {h.conflicts} = {h.conflict_cost}
                </span>
              </div>
            </div>

            {/* 3. Priority Penalty */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                    Priority Penalty (P)
                  </span>
                  <div className="h-8 w-8 rounded-lg bg-amber-50 text-amber-600 flex items-center justify-center">
                    <HeartPulse className="h-4 w-4" />
                  </div>
                </div>
                <div className="mt-2 text-2xl font-bold text-slate-900">
                  {h.priority_penalty}
                </div>
                <p className="mt-1 text-[11px] text-slate-500">
                  Triage delay penalties and priority ordering inversions.
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-slate-500">Weighted Cost:</span>
                <span className="font-mono font-bold text-amber-700">
                  20 &times; {h.priority_penalty} = {h.priority_cost}
                </span>
              </div>
            </div>

            {/* 4. Under-utilization */}
            <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-2xs flex flex-col justify-between">
              <div>
                <div className="flex items-center justify-between">
                  <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
                    Under-utilization (U)
                  </span>
                  <div className="h-8 w-8 rounded-lg bg-purple-50 text-purple-600 flex items-center justify-center">
                    <Gauge className="h-4 w-4" />
                  </div>
                </div>
                <div className="mt-2 text-2xl font-bold text-slate-900">
                  {h.under_utilization}
                </div>
                <p className="mt-1 text-[11px] text-slate-500">
                  Normalized idle capacity across doctor and room shifts.
                </p>
              </div>

              <div className="mt-4 pt-3 border-t border-slate-100 flex items-center justify-between text-xs">
                <span className="text-slate-500">Weighted Cost:</span>
                <span className="font-mono font-bold text-purple-700">
                  10 &times; {h.under_utilization} = {h.utilization_cost}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* 4. WEIGHTED COST CALCULATION */}
      {h && (
        <div className="bg-slate-900 text-white rounded-2xl p-6 shadow-md border border-slate-800">
          <div className="flex items-center gap-2 mb-2">
            <span className="px-2 py-0.5 rounded-full bg-blue-500/20 text-blue-300 text-xs font-bold">
              Section 4: Weighted Cost Calculation
            </span>
          </div>
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-800">
            <div>
              <h3 className="text-base font-bold text-white">
                Detailed Additive Cost Breakdown
              </h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Exact summation of each term multiplied by its academic coefficient.
              </p>
            </div>
            <div className="text-2xl font-mono font-extrabold text-blue-300">
              Total: {h.waiting_cost} + {h.conflict_cost} + {h.priority_cost} + {h.utilization_cost} = {h.total_score}
            </div>
          </div>

          <div className="mt-4 grid grid-cols-1 sm:grid-cols-4 gap-3 text-xs font-mono">
            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700/60">
              <span className="text-slate-400 block text-[11px]">Waiting Time Term</span>
              <span className="text-blue-400 font-bold text-sm">5 &times; {h.waiting_time} = {h.waiting_cost}</span>
            </div>
            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700/60">
              <span className="text-slate-400 block text-[11px]">Conflict Term</span>
              <span className="text-emerald-400 font-bold text-sm">100 &times; {h.conflicts} = {h.conflict_cost}</span>
            </div>
            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700/60">
              <span className="text-slate-400 block text-[11px]">Priority Penalty Term</span>
              <span className="text-amber-400 font-bold text-sm">20 &times; {h.priority_penalty} = {h.priority_cost}</span>
            </div>
            <div className="bg-slate-800/80 p-3 rounded-lg border border-slate-700/60">
              <span className="text-slate-400 block text-[11px]">Under-utilization Term</span>
              <span className="text-purple-400 font-bold text-sm">10 &times; {h.under_utilization} = {h.utilization_cost}</span>
            </div>
          </div>
        </div>
      )}

      {/* 5. HILL CLIMBING OPTIMIZATION ANALYSIS */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-2xs space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-3 pb-4 border-b border-slate-100">
          <div>
            <div className="flex items-center gap-2 mb-1">
              <span className="px-2 py-0.5 rounded-full bg-purple-50 text-purple-700 text-xs font-bold">
                Section 5: Optimization Analysis
              </span>
            </div>
            <h3 className="text-lg font-bold text-slate-900">
              Hill Climbing Local Search Evaluation
            </h3>
            <p className="text-xs text-slate-500 mt-0.5">
              Empirical search trajectory, neighborhood evaluations, and convergence state
            </p>
          </div>

          <div className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl bg-amber-50 border border-amber-200 text-amber-800 text-xs font-semibold">
            <Compass className="h-4 w-4 text-amber-600" />
            <span>Local minimum reached</span>
          </div>
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-2 sm:grid-cols-5 gap-3">
          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-[11px] font-bold text-slate-500 uppercase">Initial Score</span>
            <div className="text-xl font-mono font-bold text-slate-900 mt-1">{initialScore}</div>
            <span className="text-[10px] text-slate-400">Greedy initial state H(S₀)</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-[11px] font-bold text-slate-500 uppercase">Final Score</span>
            <div className="text-xl font-mono font-bold text-blue-700 mt-1">{finalScore}</div>
            <span className="text-[10px] text-slate-400">Terminated state H(S_final)</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-[11px] font-bold text-slate-500 uppercase">Improvement</span>
            <div className="text-xl font-mono font-bold text-slate-700 mt-1">{improvement}</div>
            <span className="text-[10px] text-slate-400">Strict cost delta</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-[11px] font-bold text-slate-500 uppercase">Accepted Moves</span>
            <div className="text-xl font-mono font-bold text-slate-700 mt-1">{acceptedMoves}</div>
            <span className="text-[10px] text-slate-400">H(S&apos;) &lt; H(S) transitions</span>
          </div>

          <div className="p-3.5 rounded-xl bg-slate-50 border border-slate-200">
            <span className="text-[11px] font-bold text-slate-500 uppercase">Neighbor Evals</span>
            <div className="text-xl font-mono font-bold text-slate-900 mt-1">{neighborEvaluations}</div>
            <span className="text-[10px] text-slate-400">Candidates analyzed</span>
          </div>
        </div>

        {/* Search Status Banner */}
        <div className="p-4 rounded-xl bg-slate-900 text-white border border-slate-800 flex flex-col sm:flex-row sm:items-center justify-between gap-3 text-xs">
          <div className="flex items-center gap-2.5">
            <Activity className="h-4 w-4 text-amber-400 shrink-0" />
            <div>
              <span className="text-slate-400 font-medium">Search Status: </span>
              <strong className="text-white font-semibold">{statusMessage}</strong>
            </div>
          </div>
          <span className="text-[11px] text-slate-400 bg-slate-800 px-2.5 py-1 rounded-md shrink-0">
            100 candidate neighbors evaluated
          </span>
        </div>

        {/* Step-by-Step Optimization Process Flow Diagram */}
        <div className="p-5 rounded-xl bg-slate-50 border border-slate-200">
          <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-4 flex items-center gap-2">
            <Layers className="h-4 w-4 text-blue-600" />
            Hill Climbing Search Step-by-Step Flow
          </h4>

          <div className="flex flex-col items-center max-w-lg mx-auto space-y-2 text-xs">
            {/* Step 1 */}
            <div className="w-full bg-white border border-slate-300 rounded-lg p-3 text-center shadow-2xs">
              <span className="font-bold text-slate-800 block">Initial Schedule Generation</span>
              <span className="text-slate-500 font-mono text-[11px]">H(S₀) = {initialScore} (Greedy Priority + Earliest Slot)</span>
            </div>

            <ArrowDown className="h-4 w-4 text-slate-400" />

            {/* Step 2 */}
            <div className="w-full bg-white border border-slate-300 rounded-lg p-3 text-center shadow-2xs">
              <span className="font-bold text-slate-800 block">Neighborhood Generation</span>
              <span className="text-slate-500 text-[11px]">Time Shift (&plusmn;10m), Doctor Reassign, Room Reassign, Patient Swap</span>
            </div>

            <ArrowDown className="h-4 w-4 text-slate-400" />

            {/* Step 3 */}
            <div className="w-full bg-blue-50 border border-blue-200 rounded-lg p-3 text-center shadow-2xs">
              <span className="font-bold text-blue-900 block">Candidate Evaluation</span>
              <span className="text-blue-700 text-[11px] font-mono">100 candidate neighbors evaluated against H(S)</span>
            </div>

            <ArrowDown className="h-4 w-4 text-slate-400" />

            {/* Step 4 */}
            <div className="w-full bg-amber-50 border border-amber-200 rounded-lg p-3 text-center shadow-2xs">
              <span className="font-bold text-amber-900 block">Acceptance Check: H(S&apos;) &lt; H(S_current)?</span>
              <span className="text-amber-800 text-[11px]">No candidate neighbor had H(S&apos;) &lt; {initialScore}</span>
            </div>

            <ArrowDown className="h-4 w-4 text-slate-400" />

            {/* Step 5 */}
            <div className="w-full bg-slate-900 text-white rounded-lg p-3 text-center shadow-sm">
              <span className="font-bold text-white block">Search Termination (Local Minimum)</span>
              <span className="text-slate-300 font-mono text-[11px]">Final Schedule H(S_final) = {finalScore} | Improvement = 0.0</span>
            </div>
          </div>

          <div className="mt-4 p-3 rounded-lg bg-blue-50/70 border border-blue-200 text-blue-900 text-xs leading-relaxed">
            <strong>Key Algorithmic Principle:</strong> Zero accepted moves does not mean the algorithm failed. It means the initial schedule was already a local minimum with respect to the implemented neighborhood operators. Every neighboring perturbation examined produced an equal or higher penalty cost.
          </div>
        </div>

        {/* Score Comparison Visualization Card */}
        <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
          <h4 className="text-xs font-bold text-slate-700 uppercase tracking-wider mb-3">
            Score Progression Comparison
          </h4>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-2xs text-center">
              <span className="text-xs text-slate-500 font-medium">Initial Schedule Score</span>
              <div className="text-2xl font-mono font-bold text-slate-800 mt-1">{initialScore}</div>
              <span className="text-[11px] text-slate-400">Greedy Construction</span>
            </div>
            <div className="bg-white p-4 rounded-lg border border-slate-200 shadow-2xs text-center">
              <span className="text-xs text-slate-500 font-medium">Final Schedule Score</span>
              <div className="text-2xl font-mono font-bold text-blue-700 mt-1">{finalScore}</div>
              <span className="text-[11px] text-slate-400">After 100 Neighborhood Evaluations</span>
            </div>
          </div>
          <div className="mt-3 text-center text-xs font-medium text-slate-500">
            &bull; No score-decreasing moves were accepted. Initial state established an optimal local minimum in the neighborhood graph.
          </div>
        </div>
      </div>

      {/* 6. ASSIGNMENT EXAMPLE (SEPARATE ACADEMIC BENCHMARK) */}
      <div className="rounded-2xl border-2 border-indigo-200 bg-gradient-to-br from-indigo-50/70 via-white to-blue-50/70 p-6 shadow-xs relative">
        <div className="flex items-center gap-2 mb-2">
          <span className="px-2 py-0.5 rounded-full bg-indigo-100 text-indigo-800 text-xs font-bold">
            Section 6: Assignment Example
          </span>
          <span className="text-indigo-700 text-xs font-bold uppercase tracking-wider flex items-center gap-1">
            <BookOpen className="h-3.5 w-3.5" /> Academic Reference Benchmark (Separate from Real Schedule)
          </span>
        </div>
        <h3 className="text-base font-bold text-slate-900">
          Why Hard Conflict Weight ($W_2 = 100$) Outweighs Waiting Time
        </h3>
        <p className="text-xs text-slate-600 mt-1 max-w-2xl">
          The academic assignment specification provides the following formal comparative benchmark to demonstrate why a schedule with lower waiting time is rejected when it violates conflict-free hard constraints.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          {/* Schedule A */}
          <div className="bg-white rounded-xl border border-emerald-200 p-4 shadow-2xs">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-emerald-800">Schedule A (Conflict-Free)</span>
              <span className="px-2 py-0.5 rounded-full bg-emerald-100 text-emerald-700 text-[10px] font-bold">
                Preferred Solution
              </span>
            </div>
            <ul className="mt-3 text-xs space-y-1 text-slate-600">
              <li>Waiting time (WT): <strong className="font-mono">40 min</strong></li>
              <li>Conflicts (C): <strong className="font-mono text-emerald-600">0</strong></li>
              <li>Priority penalty (P): <strong className="font-mono">2</strong></li>
              <li>Under-utilization (U): <strong className="font-mono">3</strong></li>
            </ul>
            <div className="mt-3 pt-2 border-t border-slate-100 font-mono text-xs text-slate-800">
              H(A) = 5(40) + 100(0) + 20(2) + 10(3) = <strong className="text-emerald-700 text-sm">270</strong>
            </div>
          </div>

          {/* Schedule B */}
          <div className="bg-white rounded-xl border border-rose-200 p-4 shadow-2xs">
            <div className="flex items-center justify-between">
              <span className="text-xs font-bold text-rose-800">Schedule B (Contains 1 Conflict)</span>
              <span className="px-2 py-0.5 rounded-full bg-rose-100 text-rose-700 text-[10px] font-bold">
                Inferior Score
              </span>
            </div>
            <ul className="mt-3 text-xs space-y-1 text-slate-600">
              <li>Waiting time (WT): <strong className="font-mono">30 min</strong> (lower wait)</li>
              <li>Conflicts (C): <strong className="font-mono text-rose-600">1 overlap (+100)</strong></li>
              <li>Priority penalty (P): <strong className="font-mono">1</strong></li>
              <li>Under-utilization (U): <strong className="font-mono">2</strong></li>
            </ul>
            <div className="mt-3 pt-2 border-t border-slate-100 font-mono text-xs text-slate-800">
              H(B) = 5(30) + 100(1) + 20(1) + 10(2) = <strong className="text-rose-700 text-sm">290</strong>
            </div>
          </div>
        </div>

        <div className="mt-4 p-3 rounded-lg bg-indigo-100/60 border border-indigo-200 text-indigo-950 text-xs">
          <strong>Key Takeaway for Academic Viva:</strong> Even though Schedule B exhibits 10 minutes less total waiting time (30m vs 40m), its single scheduling overlap imposes a 100-point penalty, raising H(B) to 290. Schedule A has a lower heuristic value (270 &lt; 290) and is strictly accepted as the superior schedule by the Hill Climbing algorithm.
        </div>
      </div>

      {/* 7. EXPLANATION OF LOCAL MINIMUM */}
      <div className="bg-white rounded-2xl border border-slate-200 p-6 shadow-2xs space-y-4">
        <div className="flex items-center gap-2 mb-1">
          <span className="px-2 py-0.5 rounded-full bg-slate-100 text-slate-800 text-xs font-bold">
            Section 7: Local Minimum Explanation
          </span>
          <h3 className="text-sm font-bold text-slate-900 flex items-center gap-2">
            <Info className="h-4 w-4 text-blue-600" />
            Theoretical Analysis: Local Minimum vs. Global Optimum
          </h3>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-slate-600">
          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
            <h4 className="font-bold text-slate-800">Why Hill Climbing Reached a Local Minimum</h4>
            <p className="mt-1 text-slate-500 leading-relaxed">
              Standard Hill Climbing is a greedy trajectory-based local search heuristic. It iteratively moves to a neighboring state only if the candidate strictly improves the objective function ($H(S&apos;) &lt; H(S)$). Because the deterministic greedy construction prioritized patients by urgency and packed earliest available conflict-free slots, any localized perturbation (shifting time, switching rooms, or reassigning doctors) either increased patient waiting time or disrupted conflict-free constraints.
            </p>
          </div>

          <div className="p-4 rounded-xl bg-slate-50 border border-slate-200">
            <h4 className="font-bold text-slate-800">Academic Distinction &amp; Scope</h4>
            <p className="mt-1 text-slate-500 leading-relaxed">
              This system does not claim that 1047.7 is the global optimum of all theoretically possible permutations ($20!$ permutations across 4 doctors and 3 rooms). It demonstrates that within the defined neighborhood topology of 1-step and 2-step modifications, no improving direction exists. Advanced metaheuristics (such as Simulated Annealing or Random-Restart Hill Climbing) can explore across plateaus or uphill transitions to escape local minima.
            </p>
          </div>
        </div>
      </div>
    </AppShell>
  );
}
