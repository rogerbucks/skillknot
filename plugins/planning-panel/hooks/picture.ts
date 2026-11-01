import type { Plan, Question } from '../types'

export type StepState = 'done' | 'now' | 'held' | 'later'

// The picture carries its own board, because a drawing cannot read the app's theme.
const COLOR = {
  board: '#171c2e',
  goal: '#2a3463',
  card: '#232a40',
  text: '#eef1f8',
  dim: '#a3adc4',
  done: '#3fb27f',
  now: '#4f8dff',
  held: '#f2a93b',
  heldCard: '#3a2f18',
  later: '#7a849c',
  limit: '#f0667a',
  limitCard: '#3a1f2a',
}

const FONT = 'system-ui, -apple-system, Segoe UI, sans-serif'
const PAD = 12
const NODE = 11
const MIN_WIDTH = 300
const MAX_WIDTH = 560
const CELL = 8

// A pane that reports no width gets the narrowest picture, which fits anywhere.
export const widthFor = (columns: number): number =>
  Number.isFinite(columns) ? Math.min(MAX_WIDTH, Math.max(MIN_WIDTH, columns * CELL)) : MIN_WIDTH

// The step a question holds up, or nothing if the number names no step.
const stepOf = (p: Plan, question: Question): number | undefined =>
  question.step !== undefined && question.step >= 1 && question.step <= p.steps.length
    ? question.step
    : undefined

// Done steps are done. A step with an open question is held. The first free step is now.
export const stepStates = (p: Plan): StepState[] => {
  const held = new Set(p.questions.map(one => stepOf(p, one)))
  let hasNow = false
  return p.steps.map((step, index) => {
    if (step.isDone) return 'done'
    if (held.has(index + 1)) return 'held'
    if (hasNow) return 'later'
    hasNow = true
    return 'now'
  })
}

export const looseQuestions = (p: Plan): Question[] =>
  p.questions.filter(one => stepOf(p, one) === undefined)

export const questionsFor = (p: Plan, step: number): Question[] =>
  p.questions.filter(one => stepOf(p, one) === step)

export const progress = (states: StepState[]): string => {
  const done = states.filter(one => one === 'done').length
  const held = states.filter(one => one === 'held').length
  const parts = [`${done} of ${states.length} done`]
  if (held > 0) parts.push(`${held} held by a question`)
  return parts.join(' · ')
}

const escape = (value: string): string =>
  value
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')

// No drawing surface measures text for us, so wrap by a generous average glyph width.
const wrap = (value: string, size: number, room: number): string[] => {
  const most = Math.max(8, Math.floor(room / (size * 0.53)))
  const lines: string[] = []
  let line = ''
  for (const word of value.split(/\s+/).flatMap(one => one.match(new RegExp(`.{1,${most}}`, 'gu')) ?? [])) {
    if (line && line.length + 1 + word.length > most) {
      lines.push(line)
      line = word
    } else {
      line = line ? `${line} ${word}` : word
    }
  }
  return line ? [...lines, line] : lines
}

const leading = (size: number): number => Math.round(size * 1.35)

const textBlock = (
  x: number,
  y: number,
  lines: string[],
  size: number,
  fill: string,
  weight = 400,
): string =>
  lines
    .map(
      (line, index) =>
        `<text x="${x}" y="${y + size + index * leading(size)}" font-size="${size}" font-weight="${weight}" fill="${fill}">${escape(line)}</text>`,
    )
    .join('')

const rect = (x: number, y: number, width: number, height: number, fill: string, stroke = ''): string =>
  `<rect x="${x}" y="${y}" width="${width}" height="${height}" rx="8" fill="${fill}"${stroke ? ` stroke="${stroke}"` : ''}/>`

const label = (x: number, y: number, value: string, fill = COLOR.dim): string =>
  `<text x="${x}" y="${y + 10}" font-size="10" font-weight="700" letter-spacing="1" fill="${fill}">${escape(value)}</text>`

const number = (x: number, y: number, value: number, fill: string): string =>
  `<text x="${x}" y="${y + 4}" font-size="11" font-weight="700" text-anchor="middle" fill="${fill}">${value}</text>`

const node = (x: number, y: number, state: StepState, index: number): string => {
  if (state === 'done') {
    return (
      `<circle cx="${x}" cy="${y}" r="${NODE}" fill="${COLOR.done}"/>` +
      `<path d="M${x - 5} ${y}l3.5 4 6.5-7.5" fill="none" stroke="${COLOR.board}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>`
    )
  }
  if (state === 'now') {
    return (
      `<circle cx="${x}" cy="${y}" r="${NODE + 3}" fill="none" stroke="${COLOR.now}" stroke-width="1.5" opacity="0.6"/>` +
      `<circle cx="${x}" cy="${y}" r="${NODE}" fill="${COLOR.now}"/>` +
      number(x, y, index, COLOR.board)
    )
  }
  if (state === 'held') {
    const reach = NODE + 2
    return (
      `<path d="M${x} ${y - reach}l${reach} ${reach}-${reach} ${reach}-${reach}-${reach}z" fill="${COLOR.held}"/>` +
      number(x, y, index, COLOR.board)
    )
  }
  return (
    `<circle cx="${x}" cy="${y}" r="${NODE - 1}" fill="${COLOR.board}" stroke="${COLOR.later}" stroke-width="2"/>` +
    number(x, y, index, COLOR.later)
  )
}

const questionCard = (
  x: number,
  y: number,
  room: number,
  text: string,
): { markup: string; height: number } => {
  const lines = wrap(text, 12, room - 38)
  const height = Math.max(30, lines.length * leading(12) + 14)
  return {
    height,
    markup:
      rect(x, y, room, height, COLOR.heldCard, COLOR.held) +
      `<circle cx="${x + 15}" cy="${y + 15}" r="8" fill="${COLOR.held}"/>` +
      `<text x="${x + 15}" y="${y + 19}" font-size="11" font-weight="700" text-anchor="middle" fill="${COLOR.board}">?</text>` +
      textBlock(x + 30, y + 6, lines, 12, COLOR.text),
  }
}

const legend = (y: number, width: number): { markup: string; height: number } => {
  const entries: [string, string, number][] = [
    ['Done', COLOR.done, 58],
    ['Now', COLOR.now, 54],
    ['Held by a question', COLOR.held, 128],
    ['Later', COLOR.later, 58],
    ['Limit', COLOR.limit, 54],
  ]
  let x = PAD
  let row = y
  const parts = entries.map(([name, color, room]) => {
    if (x + room > width - PAD) {
      x = PAD
      row += 18
    }
    const part =
      `<circle cx="${x + 5}" cy="${row + 7}" r="5" fill="${color}"/>` +
      `<text x="${x + 14}" y="${row + 11}" font-size="11" fill="${COLOR.dim}">${name}</text>`
    x += room
    return part
  })
  return { markup: parts.join(''), height: row - y + 16 }
}

export const drawPlan = (p: Plan, width: number): string => {
  const inner = width - PAD * 2
  const parts: string[] = []
  let y = PAD

  // The goal: where the route is heading.
  const goalLines = wrap(p.goal || 'Not set yet', 15, inner - 58)
  const forLines = p.audience ? wrap(`For: ${p.audience}`, 12, inner - 58) : []
  const goalHeight =
    Math.max(
      50,
      28 + goalLines.length * leading(15) + (forLines.length ? forLines.length * leading(12) + 4 : 0),
    )
  const goalX = PAD + 24
  const goalY = y + 26
  parts.push(
    rect(PAD, y, inner, goalHeight, COLOR.goal),
    `<circle cx="${goalX}" cy="${goalY}" r="14" fill="none" stroke="${COLOR.text}" stroke-width="2"/>`,
    `<circle cx="${goalX}" cy="${goalY}" r="8" fill="none" stroke="${COLOR.text}" stroke-width="2"/>`,
    `<circle cx="${goalX}" cy="${goalY}" r="3" fill="${COLOR.text}"/>`,
    label(PAD + 48, y + 8, 'GOAL'),
    textBlock(PAD + 48, y + 21, goalLines, 15, p.goal ? COLOR.text : COLOR.dim, 600),
  )
  if (forLines.length > 0) {
    parts.push(textBlock(PAD + 48, y + 25 + goalLines.length * leading(15), forLines, 12, COLOR.dim))
  }
  y += goalHeight + 12

  // Progress: one segment per step, so it reads before any words do.
  const states = stepStates(p)
  if (states.length > 0) {
    const gap = 3
    const segment = (inner - gap * (states.length - 1)) / states.length
    states.forEach((state, index) => {
      const x = PAD + index * (segment + gap)
      parts.push(
        `<rect x="${x.toFixed(1)}" y="${y}" width="${segment.toFixed(1)}" height="6" rx="3" fill="${COLOR[state]}"/>`,
      )
    })
    parts.push(textBlock(PAD, y + 9, [progress(states)], 11, COLOR.dim))
    y += 32
  }

  // The route: each step is a station, and an open question hangs off the step it holds up.
  const lineX = PAD + NODE + 3
  const cardX = lineX + NODE + 12
  const cardRoom = width - PAD - cardX
  const stops: { y: number; state: StepState }[] = []
  const stations: string[] = []
  p.steps.forEach((step, index) => {
    const state = states[index] ?? 'later'
    const lines = wrap(step.text, 13, cardRoom - 20 - (state === 'now' ? 44 : 0))
    const height = Math.max(34, lines.length * leading(13) + 16)
    const stopY = y + height / 2
    stops.push({ y: stopY, state })
    stations.push(
      rect(cardX, y, cardRoom, height, COLOR.card, state === 'now' ? COLOR.now : ''),
      textBlock(cardX + 10, y + 7, lines, 13, state === 'done' ? COLOR.dim : COLOR.text, state === 'now' ? 600 : 400),
    )
    if (state === 'now') {
      stations.push(
        `<text x="${width - PAD - 10}" y="${y + 21}" font-size="10" font-weight="700" letter-spacing="1" text-anchor="end" fill="${COLOR.now}">NOW</text>`,
      )
    }
    y += height + 8
    for (const question of questionsFor(p, index + 1)) {
      const card = questionCard(cardX + 14, y, cardRoom - 14, question.text)
      stations.push(
        `<path d="M${lineX} ${stopY}V${y + 15}H${cardX + 14}" fill="none" stroke="${COLOR.held}" stroke-width="1.5" stroke-dasharray="4 3"/>`,
        card.markup,
      )
      y += card.height + 8
    }
    stations.push(node(lineX, stopY, state, index + 1))
  })
  stops.slice(1).forEach((stop, index) => {
    const from = stops[index]
    if (!from) return
    const isWalked = from.state === 'done' && stop.state !== 'later'
    parts.push(
      `<line x1="${lineX}" y1="${from.y}" x2="${lineX}" y2="${stop.y}" stroke="${isWalked ? COLOR.done : COLOR.later}" stroke-width="3"${isWalked ? '' : ' stroke-dasharray="1 6" stroke-linecap="round"'}/>`,
    )
  })
  parts.push(...stations)
  if (p.steps.length === 0) {
    parts.push(textBlock(PAD, y, ['No steps yet'], 13, COLOR.dim))
    y += 28
  }

  // Questions no step owns yet stand apart, so they still get answered.
  const loose = looseQuestions(p)
  if (loose.length > 0) {
    y += 4
    parts.push(label(PAD, y, 'OPEN, NOT TIED TO A STEP', COLOR.held))
    y += 18
    for (const question of loose) {
      const card = questionCard(PAD, y, inner, question.text)
      parts.push(card.markup)
      y += card.height + 8
    }
  }

  // Limits: a fence around the plan, drawn once at the foot.
  if (p.limits.length > 0) {
    y += 4
    const rows = p.limits.map(one => wrap(one, 12, inner - 44))
    const height = 26 + rows.reduce((sum, lines) => sum + lines.length * leading(12) + 6, 0)
    parts.push(
      `<rect x="${PAD}" y="${y}" width="${inner}" height="${height}" rx="8" fill="${COLOR.limitCard}" stroke="${COLOR.limit}" stroke-width="1.5" stroke-dasharray="6 4"/>`,
      label(PAD + 12, y + 8, 'LIMITS', COLOR.limit),
    )
    let row = y + 24
    for (const lines of rows) {
      parts.push(
        `<circle cx="${PAD + 18}" cy="${row + 8}" r="5.5" fill="none" stroke="${COLOR.limit}" stroke-width="1.8"/>`,
        `<path d="M${PAD + 14.2} ${row + 4.2}l7.6 7.6" stroke="${COLOR.limit}" stroke-width="1.8"/>`,
        textBlock(PAD + 32, row, lines, 12, COLOR.text),
      )
      row += lines.length * leading(12) + 6
    }
    y += height + 12
  }

  const key = legend(y, width)
  parts.push(key.markup)
  y += key.height + PAD

  return [
    `<svg xmlns="http://www.w3.org/2000/svg" width="${width}" height="${y}" viewBox="0 0 ${width} ${y}" font-family="${FONT}">`,
    `<rect width="${width}" height="${y}" rx="14" fill="${COLOR.board}"/>`,
    ...parts,
    '</svg>',
  ].join('')
}
