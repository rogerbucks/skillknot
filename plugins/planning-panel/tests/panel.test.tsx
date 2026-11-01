import { expect, test } from 'claude-code/testing'
import type { TestBody } from 'claude-code/testing'

import { drawPlan, stepStates, widthFor } from '../hooks/picture'
import type { Plan } from '../types'

const PANE = {
  plugin: 'planning-panel',
  component: 'Pane',
  requestId: 'planning-panel',
  props: {
    title: 'Plan',
    isFocused: false,
    bodyColumns: 40,
    placement: 'dock',
    scroll: { offset: 0, bodyRows: 30 },
    view: {},
  },
} as const

const TOOL = 'mcp__planning-panel__update_plan'
const PICTURED = ['desktop', 'vscode', 'mobile'] as const

const engine = (on: Parameters<TestBody>[1]) => {
  // Nothing sits beneath the plugin: each hook here stands for the engine.
  on('command.register', () => ({ value: { command: 'plan-panel' } }))
  on('tool.register', () => ({ value: { tool: TOOL } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
}

const VENUE = {
  goal: 'Pick a venue for the team day',
  audience: 'Twelve people; the manager decides',
  limits: ['Under 2,000 in total', 'Step-free access'],
  open_questions: [{ text: 'Which date?', step: 2 }, 'Is catering included?'],
  next_steps: [
    { text: 'Shortlist three venues', done: true },
    'Book the venue',
    'Tell the team',
  ],
}

test('an empty panel says how it fills in, on every surface', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })

  for (const surface of ['terminal', 'desktop', 'vscode', 'mobile'] as const) {
    const ui = await $.ui.mount({ ...PANE, surface })
    expect(await ui.find({ type: 'Text', text: /Start planning/ })).toBeDefined()
    await ui.unmount()
  }
})

test('the tool answers in plain text', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })

  const reply = await $.tool.call({ tool: TOOL, ...VENUE })

  expect(reply.deny).toBeUndefined()
  // A tool's result reaches the model as text: an object is refused in a session.
  expect(typeof reply.result).toBe('string')
  expect(reply.result).toMatch(/^Panel updated\./)
  expect(reply.result).toContain('Which date? (holds up step 2)')
  expect(reply.result).toContain('1. [done] Shortlist three venues')
})

test('a graphical surface draws the plan as a picture, with the words beside it', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
  await $.tool.call({ tool: TOOL, ...VENUE })

  for (const surface of PICTURED) {
    const ui = await $.ui.mount({ ...PANE, surface })
    const picture = await ui.find({ type: 'Svg' })
    expect(picture?.props.source).toContain('Pick a venue')
    expect(picture?.props.alt).toContain('Pick a venue for the team day')
    expect(picture?.props.alt).toContain('Is catering included?')
    await ui.unmount()
  }
})

test('the terminal draws the same route in text', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })
  await $.tool.call({ tool: TOOL, ...VENUE })

  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect((await ui.find({ type: 'Text', text: /Shortlist/ }))?.text).toContain('✓ 1.')
  expect((await ui.find({ type: 'Text', text: /Book the/ }))?.text).toContain('◆ 2.')
  expect((await ui.find({ type: 'Text', text: /Which date/ }))?.text).toContain('┆ ?')
  expect((await ui.find({ type: 'Text', text: /Tell the/ }))?.text).toContain('← now')
  expect(await ui.find({ type: 'Text', text: /1 of 3 done · 1 held/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /Is catering/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /Step-free/ })).toBeDefined()
  await ui.unmount()
})

test('a later call replaces only what it sends', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })

  await $.tool.call({ tool: TOOL, ...VENUE })
  await $.tool.call({ tool: TOOL, open_questions: [] })

  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect(await ui.find({ type: 'Text', text: /venue for/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /Step-free/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /Which date/ })).toBeUndefined()
  await ui.unmount()
})

test('a repeated step keeps its done mark unless the call changes it', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })

  await $.tool.call({ tool: TOOL, next_steps: [{ text: 'First', done: true }, 'Second'] })
  await $.tool.call({ tool: TOOL, next_steps: ['First', 'Second', 'Third'] })
  let ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect((await ui.find({ type: 'Text', text: /First/ }))?.text).toContain('✓')
  await ui.unmount()

  await $.tool.call({ tool: TOOL, next_steps: [{ text: 'First', done: false }] })
  ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect((await ui.find({ type: 'Text', text: /First/ }))?.text).toContain('●')
  await ui.unmount()
})

test('clear starts a new plan', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })

  await $.tool.call({ tool: TOOL, goal: 'Old plan', next_steps: ['Old step'] })
  await $.tool.call({ tool: TOOL, clear: true, goal: 'New plan' })

  const ui = await $.ui.mount({ ...PANE, surface: 'terminal' })
  expect(await ui.find({ type: 'Text', text: /New plan/ })).toBeDefined()
  expect(await ui.find({ type: 'Text', text: /Old step/ })).toBeUndefined()
  await ui.unmount()
})

test('a value an earlier version stored is declined', async ($, on) => {
  on('state.get', () => ({ value: { value: { goal: 3 }, version: 1 } }))

  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
  expect(await ui.find({ type: 'Text', text: /Start planning/ })).toBeDefined()
  await ui.unmount()
})

test('where no pane can show, the result says to keep the plan in the chat', async ($, on) => {
  on('command.register', () => ({ value: { command: 'plan-panel' } }))
  on('tool.register', () => ({ value: { tool: TOOL } }))
  on('ui.open', () => ({ value: { isPlaced: false, reason: 'no-surface' } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })

  const ran = await $.tool.call({ tool: TOOL, goal: 'Pick a venue' })
  expect(String(ran.result)).toMatch(/^No pane can show here/)
  expect(String(ran.result)).toMatch(/Pick a venue/)
})

const plan = (change: Partial<Plan>): Plan => ({
  goal: '',
  audience: '',
  limits: [],
  questions: [],
  steps: [],
  ...change,
})

test('a question holds its step, and the first free step is the one to do now', () => {
  const steps = ['a', 'b', 'c', 'd'].map(text => ({ text, isDone: text === 'a' }))
  const held = plan({ steps, questions: [{ text: 'Why?', step: 2 }] })
  expect(stepStates(held)).toEqual(['done', 'held', 'now', 'later'])
})

test('a question naming no step holds nothing', () => {
  const steps = [{ text: 'a', isDone: false }]
  expect(stepStates(plan({ steps, questions: [{ text: 'Why?', step: 9 }] }))).toEqual(['now'])
})

test('text is escaped, so a plan cannot break out of the picture', () => {
  const picture = drawPlan(plan({ goal: '</text><script>x</script> & "more"' }), 360)
  expect(picture).not.toContain('<script>')
  expect(picture).toContain('&lt;script&gt;')
})

test('the fullest plan stays inside what the surface will take', () => {
  const text = 'word '.repeat(60).trim()
  const steps = Array.from({ length: 12 }, () => ({ text, isDone: false }))
  const questions = Array.from({ length: 12 }, (_, index) => ({ text, step: index + 1 }))
  const fullest = plan({ goal: text, audience: text, limits: Array(12).fill(text), steps, questions })
  expect(drawPlan(fullest, widthFor(1)).length).toBeLessThan(131072)
})
