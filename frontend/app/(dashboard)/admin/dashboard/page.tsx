"use client";

import {
  MessageSquare,
  MapPin,
  AlertTriangle,
  Brain,
} from "lucide-react";
import { RefreshCw } from "lucide-react";
import { StatsCard } from "@/components/dashboard/stats-card";
import { IntentChart } from "@/components/dashboard/intent-chart";
import { LocalisationChart } from "@/components/dashboard/localisation-chart";
import { TopProblems } from "@/components/dashboard/top-problems";
import { LatestReports } from "@/components/dashboard/latest-reports";
import { RecentActivity } from "@/components/dashboard/recent-activity";
export default function AdminDashboardPage() {
  return (
    <div className="space-y-6">
      <div>
        <p className="text-sm text-[#6b7280]">
          Suivi des performances de l'assitant conversationnelle
        </p>
      </div>
                 <button
            onClick={() => window.location.reload()}
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
              transition
              hover:opacity-90
            "
          >
            <RefreshCw size={16} />
            Actualiser
          </button>
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
          value="1254"
          icon={<MessageSquare size={22} />}
        />

        <StatsCard
          title="Intent principal"
          value="Facturation"
          icon={<Brain size={22} />}
        />

        <StatsCard
          title="Zone la plus active"
          value="Lomé"
          icon={<MapPin size={22} />}
        />

        <StatsCard
          title="Signalements en attente"
          value="12"
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
        <IntentChart />

        <LocalisationChart />

      </div>
      <div
  className="
    grid
    gap-6
    lg:grid-cols-2
  "
>
  <TopProblems />

  <LatestReports />
  <RecentActivity/>
</div>
    </div>
  );
}