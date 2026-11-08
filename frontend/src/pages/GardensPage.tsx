import { useState } from 'react'
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query'
import {
  createGarden, deleteGarden, listGardens, updateGarden,
  type Garden, type GardenInput,
} from '../api/gardens'
import GardenForm from '../components/GardenForm'

export default function GardensPage() {
  const queryClient = useQueryClient()
  const [editing, setEditing] = useState<Garden | 'new' | null>(null)

  const { data: gardens, isLoading, error } = useQuery({
    queryKey: ['gardens'],
    queryFn: listGardens,
  })

  const save = useMutation({
    mutationFn: (input: GardenInput) =>
      editing !== null && editing !== 'new'
        ? updateGarden(editing.id, input)
        : createGarden(input),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['gardens'] })
      setEditing(null)
    },
  })

  const remove = useMutation({
    mutationFn: deleteGarden,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ['gardens'] }),
  })

  function open(target: Garden | 'new') {
    save.reset()
    setEditing(target)
  }

  function confirmDelete(garden: Garden) {
    if (window.confirm(`Delete "${garden.name}" and all its plants?`)) {
      remove.mutate(garden.id)
    }
  }

  return (
    <div className="mx-auto max-w-4xl p-6">
      <div className="mb-4 flex items-center justify-between">
        <h1 className="text-2xl font-bold text-green-900">My gardens</h1>
        {editing === null && (
          <button onClick={() => open('new')}
            className="rounded bg-green-700 px-4 py-2 font-semibold text-white hover:bg-green-800">
            + New garden
          </button>
        )}
      </div>

      {editing !== null && (
        <div className="mb-6">
          <GardenForm
            key={editing === 'new' ? 'new' : editing.id}
            initial={editing === 'new' ? undefined : editing}
            busy={save.isPending}
            error={save.error?.message ?? null}
            onSubmit={(data) => save.mutate(data)}
            onCancel={() => setEditing(null)}
          />
        </div>
      )}

      {isLoading && <p className="text-gray-600">Loading…</p>}
      {error && <p className="text-red-600">Could not load gardens: {error.message}</p>}
      {remove.error && <p className="text-red-600">{remove.error.message}</p>}

      {gardens?.length === 0 && editing === null && (
        <p className="rounded-xl bg-white p-6 text-gray-600 shadow">
          You have no gardens yet. Create your first one to start adding plants.
        </p>
      )}

      <div className="grid gap-4 sm:grid-cols-2">
        {gardens?.map((garden) => (
          <div key={garden.id} className="rounded-xl bg-white p-4 shadow">
            <h2 className="text-lg font-semibold text-green-900">{garden.name}</h2>
            <p className="mt-1 text-sm text-gray-600">
              {garden.latitude !== null && garden.longitude !== null
                ? `Location: ${garden.latitude}, ${garden.longitude}`
                : 'No location set'}
            </p>
            {garden.timezone && (
              <p className="text-sm text-gray-600">Timezone: {garden.timezone}</p>
            )}
            <div className="mt-3 flex gap-3 text-sm">
              <button onClick={() => open(garden)} className="text-green-700 underline">
                Edit
              </button>
              <button onClick={() => confirmDelete(garden)} className="text-red-600 underline">
                Delete
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}