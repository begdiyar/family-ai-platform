import { Component, type ReactNode } from 'react'
import i18n from '@/i18n'

type Props = { children: ReactNode }
type State = { hasError: boolean; error: Error | null }

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error }
  }

  componentDidCatch(error: Error, info: { componentStack: string }) {
    console.error('[ErrorBoundary]', error, info.componentStack)
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="flex min-h-screen flex-col items-center justify-center gap-4 p-6 text-center">
          <p className="text-4xl">⚠️</p>
          <h1 className="text-xl font-semibold text-gray-900">{i18n.t('common:error_boundary_title')}</h1>
          <p className="max-w-sm text-sm text-gray-500">
            {i18n.t('common:error_boundary_desc')}
          </p>
          <button
            onClick={() => window.location.reload()}
            className="rounded-xl bg-primary px-6 py-2.5 text-sm font-medium text-white hover:opacity-90"
          >
            {i18n.t('common:error_boundary_btn')}
          </button>
          {import.meta.env.DEV && this.state.error && (
            <pre className="mt-4 max-w-xl overflow-auto rounded-lg bg-gray-100 p-4 text-left text-xs text-red-600">
              {this.state.error.message}
            </pre>
          )}
        </div>
      )
    }
    return this.props.children
  }
}
