import { expect, test } from 'claude-code/testing'
import type { TestBody } from 'claude-code/testing'

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

const engine = (on: Parameters<TestBody>[1]) => {
  // Nothing sits beneath the plugin: each hook here stands for the engine.
  on('command.register', () => ({ value: { command: 'plan-panel' } }))
  on('tool.register', () => ({ value: { tool: TOOL } }))
  on('ui.open', () => ({ value: { isPlaced: true } }))
  on('session.start', (_, e) => ({ cwd: e.cwd }))
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

test('the tool fills the panel, and a later call replaces only what it sends', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })

  await $.tool.call({
    tool: TOOL,
    goal: 'Pick a venue for the team day',
    audience: 'Twelve people; the manager decides',
    limits: ['Under 2,000 in total', 'Step-free access'],
    open_questions: ['Which date?'],
    next_steps: ['Shortlist three venues'],
  })
  const ran = await $.tool.call({ tool: TOOL, open_questions: [] })
  // A tool's result reaches the model as text: an object is refused in a session.
  expect(String(ran.result)).toMatch(/^Panel updated\./)

  for (const surface of ['terminal', 'desktop', 'vscode', 'mobile'] as const) {
    const ui = await $.ui.mount({ ...PANE, surface })
    expect((await ui.find({ type: 'Text', text: /venue for/ }))?.text).toBe(
      'Pick a venue for the team day',
    )
    expect(await ui.find({ type: 'Text', text: /Step-free/ })).toBeDefined()
    expect((await ui.find({ type: 'Text', text: /Open questions/ }))?.text).toBe(
      'Open questions (0)',
    )
    expect(await ui.find({ type: 'Text', text: /Which date/ })).toBeUndefined()
    await ui.unmount()
  }
})

test('clear starts a new plan', async ($, on) => {
  engine(on)
  await $.session.start({ cwd: '/', surface: 'desktop', isInteractive: true })

  await $.tool.call({ tool: TOOL, goal: 'Old plan', next_steps: ['Old step'] })
  await $.tool.call({ tool: TOOL, clear: true, goal: 'New plan' })

  const ui = await $.ui.mount({ ...PANE, surface: 'desktop' })
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
