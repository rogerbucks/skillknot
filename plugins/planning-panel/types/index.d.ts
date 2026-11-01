export type Step = {
  text: string
  isDone: boolean
}

export type Question = {
  text: string
  // The step it holds up, counted from 1. Absent, it is tied to no step.
  step?: number
}

export type Plan = {
  goal: string
  audience: string
  limits: string[]
  questions: Question[]
  steps: Step[]
}

declare module 'claude-code' {
  interface PluginState {
    'planning-panel': { plan: Shaped<Plan> }
  }
}
