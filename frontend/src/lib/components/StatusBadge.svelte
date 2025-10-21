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
            cssClass: 'status-online'
        },
        offline: {
            emoji: '🔴',
            label: 'Offline',
            cssClass: 'status-offline'
        },
        unknown: {
            emoji: '🟡',
            label: isChecking ? 'Checking...' : 'Unknown',
            cssClass: 'status-unknown'
        }
    }

    const config = $derived(statusConfig[status])
</script>

<div class="status-badge {config.cssClass}">
    <div class="status-dot"></div>
    <span>
        {config.emoji} {config.label}
    </span>
</div>