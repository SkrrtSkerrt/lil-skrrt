import { describe, expect, it } from 'vitest'

import { env } from '../utils/env.js'

import { needsAltScreenResizeScrollbackClear, skipKittyKeyboardProtocol } from './terminal.js'

describe('terminal resize quirks', () => {
  it('uses a deeper alt-screen resize clear for Apple Terminal', () => {
    expect(needsAltScreenResizeScrollbackClear({ TERM_PROGRAM: 'Apple_Terminal' })).toBe(true)
    expect(needsAltScreenResizeScrollbackClear({ TERM_PROGRAM: ' Apple_Terminal ' })).toBe(true)
  })

  it('keeps the normal resize repaint path for modern terminals', () => {
    expect(needsAltScreenResizeScrollbackClear({ TERM_PROGRAM: 'vscode' })).toBe(false)
    expect(needsAltScreenResizeScrollbackClear({ TERM_PROGRAM: 'iTerm.app' })).toBe(false)
  })
})

describe('skipKittyKeyboardProtocol', () => {
  it('skips the kitty protocol push for ghostty', () => {
    const saved = env.terminal
    try {
      env.terminal = 'ghostty'
      expect(skipKittyKeyboardProtocol()).toBe(true)
    } finally {
      env.terminal = saved
    }
  })

  it.each(['iTerm.app', 'kitty', 'WezTerm', 'tmux', 'windows-terminal', 'vscode'])(
    'keeps the dual push for %s',
    terminal => {
      const saved = env.terminal
      try {
        env.terminal = terminal
        expect(skipKittyKeyboardProtocol()).toBe(false)
      } finally {
        env.terminal = saved
      }
    }
  )
})
