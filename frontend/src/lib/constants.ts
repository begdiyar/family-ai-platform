import type { Zone } from '@/types/domain.types'

export const ZONE_COLORS: Record<Zone, string> = {
  communication: '#2C5678',
  trust:         '#286250',
  intimacy:      '#74364A',
  conflict:      '#744E26',
  values:        '#463E80',
  future:        '#385C8A',
}

export const ZONE_STATUS_COLORS = {
  strong:    '#386858',
  growth:    '#886028',
  attention: '#843048',
}

export const ZONE_I18N_KEYS: Record<Zone, string> = {
  communication: 'common:zones.communication',
  trust: 'common:zones.trust',
  intimacy: 'common:zones.intimacy',
  conflict: 'common:zones.conflict',
  values: 'common:zones.values',
  future: 'common:zones.future',
}
