import { useState, type FormEvent } from 'react'
import type { Garden, GardenInput } from '../api/gardens'

type Props = {
  initial?: Garden
  busy: boolean
  error: string | null
  onSubmit: (data: GardenInput) => void
  onCancel: () => void
}

function toNumber(value: string): number | null {
  return value.trim() === '' ? null : Number(value)
}

export default function GardenForm({ initial, busy, error, onSubmit, onCancel }: Props) {
  const [name, setName] = useState(initial?.name ?? '')
  const [latitude, setLatitude] = useState(initial?.latitude?.toString() ?? '')
  const [longitude, setLongitude] = useState(initial?.longitude?.toString() ?? '')
  const [timezone, setTimezone] = useState(initial?.timezone ?? '')
  const [localError, setLocalError] = useState<string | null>(null)

  function handleSubmit(event: FormEvent) {
    event.preventDefault()
    const lat = toNumber(latitude)
    const lon = toNumber(longitude)
    if (Number.isNaN(lat) || Number.isNaN(lon)) {
      setLocalError('Latitude and longitude must be numbers')
      return
    }
    setLocalError(null)
    onSubmit({
      name: name.trim(),
      latitude: lat,
      longitude: lon,
      timezone: timezone.trim() || null,
    })
  }

  const input = 'mt-1 w-full rounded border border-gray-300 p-2'

  return (
    <form onSubmit={handleSubmit} className="space-y-3 rounded-xl bg-white p-4 shadow">
      <h2 className="text-lg font-bold text-green-900">
        {initial ? 'Edit garden' : 'New garden'}
      </h2>

      <label className="block text-sm font-medium text-gray-700">
        Name
        <input required maxLength={100} value={name}
          onChange={(e) => setName(e.target.value)} className={input} />
      </label>

      <div className="grid grid-cols-2 gap-3">
        <label className="block text-sm font-medium text-gray-700">
          Latitude (optional)
          <input value={latitude} onChange={(e) => setLatitude(e.target.value)}
            placeholder="36.8" className={input} />
        </label>
        <label className="block text-sm font-medium text-gray-700">
          Longitude (optional)
          <input value={longitude} onChange={(e) => setLongitude(e.target.value)}
            placeholder="10.18" className={input} />
        </label>
      </div>

      <label className="block text-sm font-medium text-gray-700">
        Timezone (optional)
        <input value={timezone} onChange={(e) => setTimezone(e.target.value)}
          placeholder="Africa/Tunis" className={input} />
      </label>

      <p className="text-xs text-gray-500">
        The location will be used later to get weather forecasts for this garden.
      </p>

      {(localError || error) && (
        <p className="text-sm text-red-600">{localError ?? error}</p>
      )}

      <div className="flex gap-2">
        <button type="submit" disabled={busy}
          className="rounded bg-green-700 px-4 py-2 font-semibold text-white hover:bg-green-800 disabled:opacity-50">
          {busy ? 'Saving…' : 'Save'}
        </button>
        <button type="button" onClick={onCancel}
          className="rounded border border-gray-300 px-4 py-2 text-gray-700 hover:bg-gray-100">
          Cancel
        </button>
      </div>
    </form>
  )
}