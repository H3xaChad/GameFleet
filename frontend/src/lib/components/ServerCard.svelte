<script lang="ts">
    import { type GameServer, type BaseServerInfo, ServerStatus } from '$lib/api/Api'
    import StatusBadge from './StatusBadge.svelte'

    interface Props {
        server: GameServer
        liveInfo?: BaseServerInfo
        onClick?: (serverId: string) => void
    }

    let { server, liveInfo, onClick }: Props = $props()

    function handleClick() {
        if (server.id && onClick) {
            onClick(server.id)
        }
    }

    function handleKeyPress(event: KeyboardEvent) {
        if (event.key === 'Enter' && server.id && onClick) {
            onClick(server.id)
        }
    }
</script>

<div 
    class="glass-card server-card"
    onclick={handleClick}
    role="button"
    tabindex="0"
    onkeypress={handleKeyPress}
>
    <!-- Status indicator -->
    <div class="card-header">
        {#if liveInfo}
            <StatusBadge status={liveInfo.status} />
        {:else}
            <StatusBadge status={ServerStatus.Unknown} isChecking={true} />
        {/if}
    </div>

    <div class="card-body">
        <!-- Game name and info -->
        <div class="mb-4">
            <h3 class="server-title">{server.name}</h3>
            <p class="server-game">🎯 {server.game.replace('_', ' ')}</p>
        </div>

        <!-- Server details -->
        <div class="server-details">
            <div class="detail-item">
                <span class="detail-icon">🌐</span>
                <span class="detail-value">{server.address}</span>
            </div>

            {#if liveInfo && liveInfo.players_online !== null && liveInfo.players_max !== null}
                <div class="detail-item">
                    <span class="detail-icon">👥</span>
                    <span class="detail-value">{liveInfo.players_online}/{liveInfo.players_max} players</span>
                </div>
            {/if}

            {#if liveInfo && liveInfo.latency}
                <div class="detail-item">
                    <span class="detail-icon">⚡</span>
                    <span class="detail-value">{Math.trunc(liveInfo.latency)}ms</span>
                </div>
            {/if}

            {#if liveInfo && liveInfo.version}
                <div class="detail-item">
                    <span class="detail-icon">🔧</span>
                    <span class="detail-value">v{liveInfo.version}</span>
                </div>
            {/if}
        </div>

        <!-- Error message -->
        {#if liveInfo && liveInfo.error_message}
            <div class="error-message">
                ⚠️ {liveInfo.error_message}
            </div>
        {/if}
    </div>
</div>