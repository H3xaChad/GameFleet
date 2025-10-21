<script lang="ts">
    import type { ServerStatus } from '$lib/api/Api'

    interface Props {
        status: ServerStatus
        isChecking?: boolean
    }

    let { status, isChecking = false }: Props = $props()

    const statusConfig = {
        online: {
            emoji: '🟢',
            label: 'Online',
            color: 'text-game-accent-600',
            bgClass: 'bg-gradient-to-r from-game-accent-100 to-game-accent-200 border-game-accent-200',
            dotClass: 'bg-game-accent-500 animate-pulse',
            statusClass: 'status-online'
        },
        offline: {
            emoji: '🔴',
            label: 'Offline',
            color: 'text-game-error-600',
            bgClass: 'bg-gradient-to-r from-game-error-100 to-game-error-200 border-game-error-200',
            dotClass: 'bg-game-error-500',
            statusClass: 'status-offline'
        },
        unknown: {
            emoji: '🟡',
            label: isChecking ? 'Checking...' : 'Unknown',
            color: 'text-game-warning-600',
            bgClass: 'bg-gradient-to-r from-game-warning-100 to-game-warning-200 border-game-warning-200',
            dotClass: 'bg-game-warning-500 animate-pulse',
            statusClass: 'status-unknown'
        }
    }

    const config = $derived(statusConfig[status])
</script>

<div class={`inline-flex items-center px-4 py-2 rounded-full text-sm font-bold border-2 shadow-sm ${config.bgClass} ${config.statusClass}`}>
    <div class={`w-3 h-3 rounded-full mr-3 ${config.dotClass}`}></div>
    <span class={config.color}>
        {config.emoji} {config.label}
    </span>
</div>