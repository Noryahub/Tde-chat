"use client";

import { useEffect, useState } from "react";
import {
  MessageSquare,
  MapPin,
  AlertTriangle,
  Brain,
  RefreshCw,
} from "lucide-react";

import { StatsCard } from "@/components/dashboard/stats-card";
import { IntentChart } from "@/components/dashboard/intent-chart";
import { LocalisationChart } from "@/components/dashboard/localisation-chart";
import { TopProblems } from "@/components/dashboard/top-problems";
import { LatestReports } from "@/components/dashboard/latest-reports";
import { RecentActivity } from "@/components/dashboard/recent-activity";

import {
  getDashboardAnalytics,
  getLatestSignalements,
} from "@/services/analytics";

export default function AdminDashboardPage() {
  const [analytics, setAnalytics] = useState<any>(null);
  const [signalements, setSignalements] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  async function loadDashboard() {
    try {
      setLoading(true);

      const dashboardData =
        await getDashboardAnalytics();

      const reportsData =
        await getLatestSignalements();

      setAnalytics(dashboardData);
      setSignalements(reportsData);
    } catch (error) {
      console.error(error);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    loadDashboard();
  }, []);

  if (loading) {
    return (
      <div className="p-6">
        Chargement...
      </div>
    );
  }

  const topIntent =
    analytics?.top_intents?.[0]?.intent ?? "-";

  const topLocation =
    analytics?.top_localisations?.[0]?.localisation ?? "-";

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <p className="text-sm text-[#6b7280]">
          Suivi des demandes clients
        </p>

        <button
          onClick={loadDashboard}
          className="
            flex
            items-center
            gap-2
            rounded-xl
            bg-[#1D9E75]
            px-4
            py-2
            text-sm
            font-medium
            text-white
            hover:opacity-90
          "
        >
          <RefreshCw size={16} />
          Actualiser
        </button>
      </div>

      <div
        className="
          grid
          gap-4
          md:grid-cols-2
          xl:grid-cols-4
        "
      >
        <StatsCard
          title="Conversations totales"
          value={analytics.total_conversations}
          icon={<MessageSquare size={22} />}
        />

        <StatsCard
          title="Intent principal"
          value={topIntent}
          icon={<Brain size={22} />}
        />

        <StatsCard
          title="Zone la plus active"
          value={topLocation}
          icon={<MapPin size={22} />}
        />

        <StatsCard
          title="Signalements en attente"
          value={analytics.signalements_nouveaux}
          icon={<AlertTriangle size={22} />}
        />
      </div>

      <div
        className="
          grid
          gap-6
          lg:grid-cols-2
        "
      >
        <IntentChart
          data={analytics.top_intents}
        />

        <LocalisationChart
          data={analytics.top_localisations}
        />
      </div>

      <div
        className="
          grid
          gap-6
          lg:grid-cols-2
        "
      >
        <TopProblems
          data={analytics.top_problemes}
        />

        <LatestReports
          data={signalements}
        />
      </div>

      <RecentActivity
        data={analytics.conversations_par_jour}
      />
    </div>
  );
}