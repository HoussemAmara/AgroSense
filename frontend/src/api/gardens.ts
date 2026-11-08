import { request } from './client'

export type Garden = {
  id: number
  name: string
  latitude: number | null
  longitude: number | null
  timezone: string | null
  created_at: string
}

export type GardenInput = Omit<Garden, 'id' | 'created_at'>

export const listGardens = () => request<Garden[]>('/gardens')

export const createGarden = (data: GardenInput) =>
  request<Garden>('/gardens', { method: 'POST', body: JSON.stringify(data) })

export const updateGarden = (id: number, data: GardenInput) =>
  request<Garden>(`/gardens/${id}`, { method: 'PATCH', body: JSON.stringify(data) })

export const deleteGarden = (id: number) =>
  request<void>(`/gardens/${id}`, { method: 'DELETE' })