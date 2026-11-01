export type Plan = {
  goal: string
  audience: string
  limits: string[]
  questions: string[]
  steps: string[]
}

declare module 'claude-code' {
  interface PluginState {
    'planning-panel': { plan: Shaped<Plan> }
  }
}
