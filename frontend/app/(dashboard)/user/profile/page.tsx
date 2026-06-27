"use client";

import { useAuth } from "@/hooks/use-auth";
import { FormEvent, useEffect, useRef, useState } from "react";
import {getResolvedSignalements, getUserSignalements} from "@/services/ticket-service"

export default function UserProfilePage() {
  const { user } = useAuth();
  const [isEditing, setEditing] = useState(false);
  const [isChangingPassword, changingPassword] = useState(false);
  const [loading, setLoading] = useState(false);

  const [userStats, setUserStats] = useState({
        totalSignalements: 0,
        activeSignalements: 0,
        effectiveResolutuions: 0,
      })

  const [formData, setFormData] = useState({
      nom: '',
      prenom: '',
      });
  const [passwordData, setPasswordData] = useState({
      currentPassword: '',
      newPassword: '',
      confirmedPassword:''
      });
  // user , data stats
  useEffect(()=>{
      if(user){
          setFormData({
                nom: user.nom || '',
                email: user.email || ''
            });
            loadUserStats();
          }
      },[user]);
  const loadUserStats = async () => {
        try {
            const [signalementsData, resolutuionsData] = await Promise.all([
                getUserSignalements(user.id),
                getResolvedSignalements(user.id)
            ]);

            const activeSignalements = activeSignalements.filter(signalements => !signalements.returnDate);
            const effectiveResolutuions = resolutuionsData.filter(res => res.status !== 'resolu');

            setUserStats({
                totalSignalements: signalementsData.length,
                activeSignalements: activeResolutuions.lenght,
                effectiveResolutuions: effectiveResolutuions.length,
            });
        } catch (error) {
            console.error("Error loading user stats:", error);
        }
    };
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-semibold tracking-tight">Profil</h1>
        <p className="mt-1 text-sm text-muted-foreground">Informations de votre compte.</p>
      </div>
      <section className="max-w-xl rounded-lg border bg-card p-5">
        <div className="space-y-4 text-sm">
          <p className="flex justify-between gap-4"><span className="text-muted-foreground">Nom</span><strong>{user?.name}</strong></p>
          <p className="flex justify-between gap-4"><span className="text-muted-foreground">Email</span><strong>{user?.email}</strong></p>
          <p className="flex justify-between gap-4"><span className="text-muted-foreground">Role</span><strong>{user?.role}</strong></p>
        </div>
      </section>
    </div>
  );
}
