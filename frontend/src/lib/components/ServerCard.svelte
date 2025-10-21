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
    class="glass-card rounded-2xl shadow-game border border-white/50 hover:shadow-game-xl transition-game cursor-pointer transform hover:-translate-y-2 hover:scale-105 game-card"
    onclick={handleClick}
    role="button"
    tabindex="0"
    onkeypress={handleKeyPress}
>
    <!-- Status indicator -->
    <div class="p-6 pb-4">
        {#if liveInfo}
            <StatusBadge status={liveInfo.status} />
        {:else}
            <StatusBadge status={ServerStatus.Unknown} isChecking={true} />
        {/if}
    </div>

    <div class="px-6 pb-6">
        <!-- Game name and info -->
        <div class="mb-4">
            <h3 class="font-bold text-slate-800 text-xl leading-tight mb-2 text-shadow">{server.name}</h3>
            <p class="text-base text-slate-600 capitalize font-medium">🎯 {server.game.replace('_', ' ')}</p>
        </div>

        <!-- Server details -->
        <div class="space-y-3 text-sm">
            <div class="flex items-center text-slate-600 bg-slate-50 p-3 rounded-lg backdrop-blur-game">
                <span class="mr-3 font-semibold">🌐</span>
                <span class="font-mono">{server.address}</span>
            </div>

            {#if liveInfo && liveInfo.players_online !== null && liveInfo.players_max !== null}
                <div class="flex items-center text-slate-600 bg-slate-50 p-3 rounded-lg backdrop-blur-game">
                    <span class="mr-3 font-semibold">👥</span>
                    <span class="font-semibold">{liveInfo.players_online}/{liveInfo.players_max} players</span>
                </div>
            {/if}

            {#if liveInfo && liveInfo.latency}
                <div class="flex items-center text-slate-600 bg-slate-50 p-3 rounded-lg backdrop-blur-game">
                    <span class="mr-3 font-semibold">⚡</span>
                    <span class="font-semibold">{Math.trunc(liveInfo.latency)}ms</span>
                </div>
            {/if}

            {#if liveInfo && liveInfo.version}
                <div class="flex items-center text-slate-600 bg-slate-50 p-3 rounded-lg backdrop-blur-game">
                    <span class="mr-3 font-semibold">🔧</span>
                    <span class="font-semibold">v{liveInfo.version}</span>
                </div>
            {/if}
        </div>

        <!-- Error message -->
        {#if liveInfo && liveInfo.error_message}
            <div class="mt-4 p-3 bg-gradient-to-r from-game-error-50 to-game-error-100 border border-game-error-200 rounded-lg text-xs text-game-error-700 font-medium">
                ⚠️ {liveInfo.error_message}
            </div>
        {/if}
    </div>
</div>