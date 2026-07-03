import confetti from 'canvas-confetti'

const BRAND_COLORS = ['#3C3888', '#385C8A', '#386858', '#885040', '#886028', '#DAD6EE']

export function celebrateSmall(originEl?: HTMLElement) {
  const origin = originEl
    ? {
        x: (originEl.getBoundingClientRect().left + originEl.offsetWidth / 2) / window.innerWidth,
        y: (originEl.getBoundingClientRect().top + originEl.offsetHeight / 2) / window.innerHeight,
      }
    : { x: 0.5, y: 0.6 }

  confetti({
    particleCount: 40,
    spread: 60,
    origin,
    colors: BRAND_COLORS,
    scalar: 0.8,
    gravity: 1.2,
    ticks: 120,
  })
}

export function celebrateMedium() {
  confetti({
    particleCount: 80,
    spread: 80,
    origin: { x: 0.5, y: 0.55 },
    colors: BRAND_COLORS,
    scalar: 1,
    gravity: 1,
    ticks: 160,
  })
}

export function celebrateBig() {
  const fire = (particleRatio: number, opts: confetti.Options) => {
    confetti({
      ...opts,
      origin: { y: 0.65 },
      particleCount: Math.floor(200 * particleRatio),
      colors: BRAND_COLORS,
    })
  }
  fire(0.25, { spread: 26, startVelocity: 55 })
  fire(0.2,  { spread: 60 })
  fire(0.35, { spread: 100, decay: 0.91, scalar: 0.8 })
  fire(0.1,  { spread: 120, startVelocity: 25, decay: 0.92, scalar: 1.2 })
  fire(0.1,  { spread: 120, startVelocity: 45 })
}
