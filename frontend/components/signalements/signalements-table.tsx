"use client";

import { useEffect, useMemo, useState } from "react";

import { Search } from "lucide-react";

import { getTickets } from "@/services/ticket-service";

import type { Ticket } from "@/types";

export default function SignalementsTable() {

const [tickets, setTickets] =
useState<Ticket[]>([]);

const [loading, setLoading] =
useState(true);

const [search, setSearch] =
useState("");

const [statusFilter, setStatusFilter] =
useState("all");

const [dateFilter, setDateFilter] =
useState("recent");

useEffect(() => {


async function loadTickets() {

  try {

    const response =
      await getTickets();

    setTickets(response.data);

  } catch (error) {

    console.error(error);

  } finally {

    setLoading(false);

  }

}

loadTickets();

}, []);

const filteredTickets =
useMemo(() => {


  const filtered =
    tickets.filter((ticket) => {

      const matchesSearch =

        ticket.ticket_number
          ?.toLowerCase()
          .includes(search.toLowerCase())

        ||

        ticket.localisation
          ?.toLowerCase()
          .includes(search.toLowerCase())

        ||

        ticket.description
          ?.toLowerCase()
          .includes(search.toLowerCase())

        ||

        ticket.intent
          ?.toLowerCase()
          .includes(search.toLowerCase());

      const matchesStatus =

        statusFilter === "all"
          ? true
          : ticket.statut === statusFilter;

      return (
        matchesSearch &&
        matchesStatus
      );

    });

  filtered.sort((a, b) => {

    const dateA =
      new Date(a.created_at).getTime();

    const dateB =
      new Date(b.created_at).getTime();

    return dateFilter === "recent"
      ? dateB - dateA
      : dateA - dateB;

  });

  return filtered;

}, [
  tickets,
  search,
  statusFilter,
  dateFilter,
]);


function getStatusBadge(
statut: string
) {

switch (statut) {

  case "ouvert":

    return (
      <span
        className="
          rounded-full
          bg-red-100
          px-3
          py-1
          text-xs
          font-medium
          text-red-600
        "
      >
        Ouvert
      </span>
    );

  case "en_cours":

    return (
      <span
        className="
          rounded-full
          bg-yellow-100
          px-3
          py-1
          text-xs
          font-medium
          text-yellow-700
        "
      >
        En cours
      </span>
    );

  case "resolu":

    return (
      <span
        className="
          rounded-full
          bg-green-100
          px-3
          py-1
          text-xs
          font-medium
          text-green-700
        "
      >
        Résolu
      </span>
    );

  case "cloture":

    return (
      <span
        className="
          rounded-full
          bg-gray-100
          px-3
          py-1
          text-xs
          font-medium
          text-gray-700
        "
      >
        Clôturé
      </span>
    );

  default:

    return statut;

}


}

if (loading) {


return (

  <div
    className="
      rounded-2xl
      bg-white
      p-8
      shadow-sm
    "
  >
    Chargement...
  </div>

);


}

return (

<div
  className="
    rounded-2xl
    bg-white
    p-6
    shadow-sm
  "
>

  <div
    className="
      mb-6
      flex
      flex-col
      gap-4
      lg:flex-row
      lg:items-center
      lg:justify-between
    "
  >

    <div>

      <h2
        className="
          text-lg
          font-bold
          text-slate-900
        "
      >
        Signalements
      </h2>

      <p
        className="
          text-sm
          text-slate-500
        "
      >
        {filteredTickets.length}
        {" "}
        tickets trouvés
      </p>

    </div>

    <div
      className="
        flex
        flex-col
        gap-3
        md:flex-row
      "
    >

      <div
        className="
          relative
        "
      >

        <Search
          size={18}
          className="
            absolute
            left-3
            top-1/2
            -translate-y-1/2
            text-slate-400
          "
        />

        <input
          type="text"
          placeholder="Rechercher..."
          value={search}
          onChange={(e) =>
            setSearch(
              e.target.value
            )
          }
          className="
            w-72
            rounded-lg
            border
            border-slate-200
            py-2
            pl-10
            pr-4
            text-sm
          "
        />

      </div>

      <select
        value={statusFilter}
        onChange={(e) =>
          setStatusFilter(
            e.target.value
          )
        }
        className="
          rounded-lg
          border
          border-slate-200
          px-4
          py-2
          text-sm
        "
      >

        <option value="all">
          Tous les statuts
        </option>

        <option value="ouvert">
          Ouvert
        </option>

        <option value="en_cours">
          En cours
        </option>

        <option value="resolu">
          Résolu
        </option>

        <option value="cloture">
          Clôturé
        </option>

      </select>

      <select
        value={dateFilter}
        onChange={(e) =>
          setDateFilter(
            e.target.value
          )
        }
        className="
          rounded-lg
          border
          border-slate-200
          px-4
          py-2
          text-sm
        "
      >

        <option value="recent">
          Plus récents
        </option>

        <option value="ancien">
          Plus anciens
        </option>

      </select>

    </div>

  </div>

  <div className="overflow-x-auto">

    <table
      className="
        w-full
        text-sm
      "
    >

      <thead>

        <tr
          className="
            border-b
            text-left
            text-slate-500
          "
        >

          <th className="py-4">
            Ticket
          </th>

          <th>
            Catégorie
          </th>

          <th>
            Téléphone
          </th>

          <th>
            Localisation
          </th>

          <th>
            Description
          </th>

          <th>
            Statut
          </th>

          <th>
            Date
          </th>

        </tr>

      </thead>

      <tbody>

        {filteredTickets.map(
          (ticket) => (

            <tr
              key={ticket.id}
              className="
                border-b
                transition
                hover:bg-slate-50
                cursor-pointer
              "
            >

              <td
                className="
                  py-4
                  font-medium
                "
              >
                {ticket.ticket_number}
              </td>

              <td>

                <span
                  className="
                    rounded-full
                    bg-blue-100
                    px-3
                    py-1
                    text-xs
                    font-medium
                    text-blue-700
                  "
                >
                  {ticket.intent || "Autre"}
                </span>

              </td>

              <td>
                {ticket.telephone}
              </td>

              <td>
                {ticket.localisation}
              </td>

              <td
                className="
                  max-w-xs
                  truncate
                "
              >
                {ticket.description}
              </td>

              <td>
                {getStatusBadge(
                  ticket.statut
                )}
              </td>

              <td>
                {new Date(
                  ticket.created_at
                ).toLocaleDateString()
                }
              </td>

            </tr>

          )
        )}

      </tbody>

    </table>

  </div>

</div>


);

}
