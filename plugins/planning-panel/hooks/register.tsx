import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Plan } from '../types'

const PLUGIN = 'planning-panel'
const PANE = 'planning-panel'
const TITLE = 'Plan'
const TOOL = 'update_plan'
const MAX_ITEMS = 12
const MAX_TEXT = 300

const EMPTY: Plan = {
  goal: '',
  audience: '',
  limits: [],
  questions: [],
  steps: [],
}

// Change the tag when Plan's fields change: it declines what an earlier
// version stored, which outlives a reload.
const plan = atom({ plugin: 'planning-panel', key: 'plan' } as const, EMPTY, {
  shape: 'plan-1',
})

const DESCRIPTION = [
  'Keep the planning panel beside the chat current. Call it whenever the person',
  'is planning something (a project, document, deck, design, trip or decision)',
  'and the goal, audience, limits, open questions or next steps change, including',
  'while a design-brief or slide-storyline skill runs. Send only the fields that',
  'changed: each list you send replaces that list whole. Keep every item to one',
  'short plain sentence. Remove a question once it is answered and move its',
  'answer into the goal, audience or limits. Set clear to start a new plan.',
  'The panel only shows text; it sends and stores nothing elsewhere.',
].join(' ')

const list = {
  type: 'array',
  items: { type: 'string', maxLength: MAX_TEXT },
  maxItems: MAX_ITEMS,
}

const SCHEMA = {
  type: 'object',
  properties: {
    goal: {
      type: 'string',
      maxLength: MAX_TEXT,
      description: 'What the plan is for, in one sentence: the job or the decision',
    },
    audience: {
      type: 'string',
      maxLength: MAX_TEXT,
      description: 'Who it is for or who decides, and what they need',
    },
    limits: { ...list, description: 'Musts, won\'ts, budget, deadline, rules' },
    open_questions: { ...list, description: 'What is still undecided or unknown' },
    next_steps: { ...list, description: 'The next actions, in order' },
    clear: { type: 'boolean', description: 'Empty the panel before applying the rest' },
  },
  additionalProperties: false,
}

type Change = {
  goal?: unknown
  audience?: unknown
  limits?: unknown
  open_questions?: unknown
  next_steps?: unknown
  clear?: unknown
}

const text = (value: unknown, fallback: string): string =>
  typeof value === 'string' ? value.trim().slice(0, MAX_TEXT) : fallback

const items = (value: unknown, fallback: string[]): string[] =>
  Array.isArray(value)
    ? value
        .filter((one): one is string => typeof one === 'string')
        .map(one => one.trim().slice(0, MAX_TEXT))
        .filter(one => one.length > 0)
        .slice(0, MAX_ITEMS)
    : fallback

export const applyChange = (before: Plan, change: Change): Plan => {
  const base = change.clear === true ? EMPTY : before
  return {
    goal: text(change.goal, base.goal),
    audience: text(change.audience, base.audience),
    limits: items(change.limits, base.limits),
    questions: items(change.open_questions, base.questions),
    steps: items(change.next_steps, base.steps),
  }
}

export const asMarkdown = (p: Plan): string => {
  const section = (title: string, lines: string[]) =>
    lines.length === 0 ? [] : [`**${title}:**`, ...lines.map(one => `- ${one}`)]
  return [
    `**Goal:** ${p.goal || '(not set)'}`,
    `**Audience:** ${p.audience || '(not set)'}`,
    ...section('Limits', p.limits),
    ...section('Open questions', p.questions),
    ...section('Next steps', p.steps),
  ].join('\n')
}

export const register: Register = on => {
  on('session.start', async ($, e, next) => {
    await $.command.register({
      name: 'plan-panel',
      description: 'Open the planning panel. "clear" empties it, "copy" prints it as Markdown',
    })
    await $.tool.register({
      name: TOOL,
      description: DESCRIPTION,
      inputSchema: SCHEMA,
      isDeferred: false,
    })

    return next(e)
  })

  on('command.run', { command: 'plan-panel' }, async ($, e) => {
    const word = e.args.trim().toLowerCase()
    if (word === 'clear') {
      await update($, plan, () => EMPTY)
      return { text: 'Planning panel cleared.' }
    }
    if (word === 'copy') {
      return { text: asMarkdown(await read($, plan)) }
    }
    await $.ui.open({ id: PANE, title: TITLE })
    return { text: 'Planning panel opened. It fills in as you plan.' }
  })

  on('tool.call', { tool: 'mcp__planning-panel__update_plan' }, async ($, e) => {
    const after = await update($, plan, before => applyChange(before, e as Change))
    const { isPlaced } = await $.ui.open({ id: PANE, title: TITLE })
    // Where nothing draws panes (a headless run, an app view without them), say
    // so, so the model keeps the plan visible in the chat instead.
    const where = isPlaced
      ? 'Panel updated.'
      : 'No pane can show here, so show this plan in the chat when it changes.'

    return { result: `${where}\n${asMarkdown(after)}` }
  }).catch(() => ({ deny: 'The planning panel could not update. Carry on in the chat.' }))

  on('ui.render', { component: 'Pane', requestId: PANE }, async ($, e) => {
    const { Box, Text } = $.ui.resolve(e)
    const p = await read($, plan)
    const isEmpty =
      !p.goal && !p.audience && p.limits.length + p.questions.length + p.steps.length === 0

    const field = (label: string, value: string) => (
      <Box flexDirection="column" marginBottom={1}>
        <Text bold>{label}</Text>
        {value ? <Text>{value}</Text> : <Text dimColor>Not set yet</Text>}
      </Box>
    )
    const group = (label: string, lines: string[], mark: string) => (
      <Box flexDirection="column" marginBottom={1}>
        <Text bold>
          {label} ({lines.length})
        </Text>
        {lines.length === 0 && <Text dimColor>None yet</Text>}
        {lines.map(one => (
          <Text>
            {mark} {one}
          </Text>
        ))}
      </Box>
    )

    if (isEmpty) {
      return (
        <Box flexDirection="column">
          <Text dimColor>Start planning in the chat and this fills in.</Text>
          <Text dimColor>Goal, audience, limits, open questions, next steps.</Text>
        </Box>
      )
    }

    return (
      <Box flexDirection="column">
        {field('Goal', p.goal)}
        {field('Audience', p.audience)}
        {group('Limits', p.limits, '-')}
        {group('Open questions', p.questions, '?')}
        {group('Next steps', p.steps, '>')}
      </Box>
    )
  })
}
