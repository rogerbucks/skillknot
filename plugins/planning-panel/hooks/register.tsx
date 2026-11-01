import { atom, read, update } from 'claude-code'
import type { Register } from 'claude-code'

import type { Plan, Question, Step } from '../types'
import {
  drawPlan,
  looseQuestions,
  progress,
  questionsFor,
  stepStates,
  widthFor,
} from './picture'
import type { StepState } from './picture'

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
  shape: 'plan-2',
})

const DESCRIPTION = [
  'Keep the planning panel beside the chat current. Call it whenever the person',
  'is planning something (a project, document, deck, design, trip or decision)',
  'and the goal, audience, limits, open questions or next steps change, including',
  'while a design-brief or slide-storyline skill runs. Send only the fields that',
  'changed: each list you send replaces that list whole. Keep every item to one',
  'short plain sentence. Remove a question once it is answered and move its',
  'answer into the goal, audience or limits. Tie a question to the step it holds',
  'up by giving that step\'s number, counted from 1, and send the questions again',
  'if the steps are renumbered. Mark a finished step done rather than removing it,',
  'so the panel shows progress. Set clear to start a new plan. The panel only',
  'draws what you send; it sends and stores nothing elsewhere.',
].join(' ')

const line = { type: 'string', maxLength: MAX_TEXT }

const list = {
  type: 'array',
  items: line,
  maxItems: MAX_ITEMS,
}

const listOf = (shape: Record<string, unknown>) => ({
  type: 'array',
  items: {
    anyOf: [
      line,
      {
        type: 'object',
        properties: { text: line, ...shape },
        required: ['text'],
        additionalProperties: false,
      },
    ],
  },
  maxItems: MAX_ITEMS,
})

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
    open_questions: {
      ...listOf({
        step: { type: 'integer', minimum: 1, description: 'The step it holds up, counted from 1' },
      }),
      description: 'What is still undecided or unknown: a sentence, or { text, step }',
    },
    next_steps: {
      ...listOf({ done: { type: 'boolean', description: 'True once the step is finished' } }),
      description: 'The next actions, in order: a sentence, or { text, done }',
    },
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

type Entry = { text?: unknown; step?: unknown; done?: unknown }

const entries = (value: unknown[]): (Entry & { text: string })[] =>
  value
    .map(one => (typeof one === 'string' ? { text: one } : ((one ?? {}) as Entry)))
    .filter((one): one is Entry & { text: string } => typeof one.text === 'string')
    .map(one => ({ ...one, text: one.text.trim().slice(0, MAX_TEXT) }))
    .filter(one => one.text.length > 0)
    .slice(0, MAX_ITEMS)

const questions = (value: unknown, fallback: Question[]): Question[] =>
  Array.isArray(value)
    ? entries(value).map(({ text, step }) =>
        Number.isInteger(step) ? { text, step: step as number } : { text },
      )
    : fallback

// A bare sentence keeps the done mark of the step it repeats, so adding a step undoes nothing.
// Each earlier step is matched once, so two steps with the same wording keep their own marks.
const steps = (value: unknown, fallback: Step[]): Step[] => {
  if (!Array.isArray(value)) return fallback
  const unmatched = [...fallback]
  return entries(value).map(({ text, done }) => {
    const at = unmatched.findIndex(one => one.text === text)
    const [before] = at < 0 ? [] : unmatched.splice(at, 1)
    return { text, isDone: typeof done === 'boolean' ? done : (before?.isDone ?? false) }
  })
}

export const applyChange = (before: Plan, change: Change): Plan => {
  const base = change.clear === true ? EMPTY : before
  return {
    goal: text(change.goal, base.goal),
    audience: text(change.audience, base.audience),
    limits: items(change.limits, base.limits),
    questions: questions(change.open_questions, base.questions),
    steps: steps(change.next_steps, base.steps),
  }
}

export const asMarkdown = (p: Plan): string => {
  const section = (title: string, lines: string[]) =>
    lines.length === 0 ? [] : [`**${title}:**`, ...lines.map(one => `- ${one}`)]
  const asked = (one: Question) => {
    const isTied = questionsFor(p, one.step ?? 0).includes(one)
    return isTied ? `${one.text} (holds up step ${one.step})` : one.text
  }
  return [
    `**Goal:** ${p.goal || '(not set)'}`,
    `**Audience:** ${p.audience || '(not set)'}`,
    ...section('Limits', p.limits),
    ...section('Open questions', p.questions.map(asked)),
    ...section(
      'Next steps',
      p.steps.map((one, index) => `${index + 1}. ${one.isDone ? '[done] ' : ''}${one.text}`),
    ),
  ].join('\n')
}

const MARK: Record<StepState, string> = { done: '✓', now: '●', held: '◆', later: '○' }
const TONE: Record<StepState, string> = {
  done: 'success',
  now: 'suggestion',
  held: 'warning',
  later: 'inactive',
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

    if (isEmpty) {
      return (
        <Box flexDirection="column">
          <Text dimColor>Start planning in the chat and this fills in.</Text>
          <Text dimColor>Goal, audience, limits, open questions, next steps.</Text>
        </Box>
      )
    }

    if (e.surface !== 'terminal') {
      const { Svg } = $.ui.resolve(e)
      return <Svg source={drawPlan(p, widthFor(e.props.bodyColumns))} alt={asMarkdown(p)} />
    }

    // The terminal has no vector drawing, so the same route is drawn in coloured text.
    const states = stepStates(p)
    const asked = (one: Question) => (
      <Text color="warning">
        {'  ┆ ? '}
        {one.text}
      </Text>
    )
    return (
      <Box flexDirection="column">
        <Text bold>◎ {p.goal || 'Goal not set yet'}</Text>
        {p.audience && <Text dimColor>{`  For: ${p.audience}`}</Text>}
        {states.length > 0 && (
          <Box marginTop={1} flexDirection="column">
            <Text>
              {states.map(state => (
                <Text color={TONE[state]}>██</Text>
              ))}
            </Text>
            <Text dimColor>{progress(states)}</Text>
          </Box>
        )}
        <Box marginTop={1} flexDirection="column">
          {p.steps.length === 0 && <Text dimColor>No steps yet</Text>}
          {p.steps.map((one, index) => {
            const state = states[index] ?? 'later'
            return (
              <Box flexDirection="column">
                <Text color={TONE[state]} dimColor={state === 'done'}>
                  {MARK[state]} {index + 1}. {one.text}
                  {state === 'now' ? '  ← now' : ''}
                </Text>
                {questionsFor(p, index + 1).map(asked)}
              </Box>
            )
          })}
        </Box>
        {looseQuestions(p).length > 0 && (
          <Box marginTop={1} flexDirection="column">
            <Text color="warning" bold>
              Open, not tied to a step
            </Text>
            {looseQuestions(p).map(asked)}
          </Box>
        )}
        {p.limits.length > 0 && (
          <Box marginTop={1} flexDirection="column" borderStyle="dashed" borderColor="error">
            <Text color="error" bold>
              Limits
            </Text>
            {p.limits.map(one => (
              <Text>⊘ {one}</Text>
            ))}
          </Box>
        )}
      </Box>
    )
  })
}
