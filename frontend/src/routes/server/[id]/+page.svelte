<script lang="ts">
    import { page } from '$app/state'
    import { api } from '$lib/api/ApiService'
    import type { GameServer, BaseServerInfo, ServerStatus } from '$lib/api/Api'
    import { onMount, onDestroy } from 'svelte'
    import StatusBadge from '$lib/components/StatusBadge.svelte'
    import LoadingSpinner from '$lib/components/LoadingSpinner.svelte'
    import StatCard from '$lib/components/StatCard.svelte'
    import MinecraftMOTD from '$lib/components/MinecraftMOTD.svelte'
    import ThemeToggle from '$lib/components/ThemeToggle.svelte'

    let server = $state<GameServer | null>(null)
    let liveInfo = $state<BaseServerInfo | null>(null)
    let loading = $state<boolean>(true)
    let error = $state<string | null>(null)
    let refreshInterval: ReturnType<typeof setInterval>

    const serverId = page.params.id

    async function fetchServerData() {
        if (!serverId) {
            error = 'Server ID is required'
            loading = false
            return
        }
        try {
            const [serverResponse, liveResponse] = await Promise.all([
                api.serverId.getServerById(serverId),
                api.serverId.getServerLiveInfoById(serverId)
            ])
            server = serverResponse.data
            liveInfo = liveResponse.data
            error = null
        } catch (err) {
            console.error('Failed to fetch server data:', err)
            error = 'Failed to load server information'
        } finally {
            loading = false
        }
    }

    async function refreshLiveInfo() {
        if (!serverId) return
        
        try {
            const response = await api.serverId.getServerLiveInfoById(serverId)
            liveInfo = response.data
        } catch (err) {
            console.error('Failed to refresh live info:', err)
        }
    }

    onMount(() => {
        fetchServerData()
        refreshInterval = setInterval(refreshLiveInfo, 30000)
    })

    onDestroy(() => {
        if (refreshInterval) {
            clearInterval(refreshInterval)
        }
    })

    function goBack() {
        window.history.back()
    }
</script>

<svelte:head>
    <title>{server ? server.name : 'Server Details'} - Game Server Dashboard</title>
</svelte:head>

<div class="server-detail-container">
    <!-- Background pattern -->
    <div class="background-pattern"></div>
    
    <!-- Header -->
    <div class="server-detail-header">
        <div class="server-detail-header-content">
            <div class="flex items-center justify-between">
                <div class="flex items-center">
                    <button 
                        onclick={goBack}
                        class="back-button"
                        aria-label="Go back"
                        title="Go back"
                    >
                        <span class="text-xl font-semibold text-shadow">← Back</span>
                    </button>
                    <h1 class="detail-page-title">
                        🎮 Server Details
                    </h1>
                </div>
                <ThemeToggle />
            </div>
        </div>
    </div>

    <div class="server-detail-content">
        {#if loading}
            <!-- Loading state -->
            <div class="loading-container">
                <LoadingSpinner size="md" message="🔍 Loading server information..." />
            </div>
        {:else if error}
            <!-- Error state -->
            <div class="empty-state">
                <div class="empty-state-icon">😕</div>
                <h3 class="empty-state-title">Oops! Something went wrong</h3>
                <p class="empty-state-description">{error}</p>
                <button 
                    onclick={goBack}
                    class="btn-game"
                >
                    🏠 Go Back Home
                </button>
            </div>
        {:else if server && liveInfo}
            <!-- Server information -->
            <div class="space-y-8">
                <!-- Server header -->
                <div class="glass-card card-content server-header-card">
                    <div class="server-main-info">
                        <h2>{server.name}</h2>
                        <p class="server-game-type">🎯 {server.game.replace('_', ' ')}</p>
                        <p class="server-address">🌐 {server.address}:{server.port}</p>
                    </div>
                    
                    <!-- Status badge -->
                    <div>
                        <StatusBadge status={liveInfo.status} />
                    </div>
                </div>

                <!-- Server stats grid -->
                <div class="stats-grid-detail">
                    <!-- Players -->
                    <StatCard
                        icon="👥"
                        title="Players"
                        value={liveInfo.players_online ?? 'N/A'}
                        subtitle={liveInfo.players_max ? `/ ${liveInfo.players_max}` : undefined}
                        bgColor="primary"
                    />

                    <!-- Latency -->
                    {#if liveInfo.latency !== null}
                        <StatCard
                            icon="⚡"
                            title="Latency"
                            value="{Math.trunc(liveInfo.latency ?? 0)}ms"
                            bgColor="accent"
                        />
                    {/if}

                    <!-- Version -->
                    {#if liveInfo.version}
                        <StatCard
                            icon="🔧"
                            title="Version"
                            value={liveInfo.version}
                            bgColor="secondary"
                            type="version"
                        />
                    {/if}

                    <!-- Security info -->
                    <div class="glass-card server-card">
                        <div class="security-card-component">
                            <div class="stat-icon warning">
                                <span>🔒</span>
                            </div>
                            <div class="stat-info">
                                <p class="stat-title">Security</p>
                                <div class="security-details">
                                    {#if liveInfo.password_protected !== null}
                                        <p class="security-item">
                                            {liveInfo.password_protected ? '🔐 Password Required' : '🔓 No Password'}
                                        </p>
                                    {/if}
                                    {#if liveInfo.anti_cheat_enabled !== null}
                                        <p class="security-item">
                                            {liveInfo.anti_cheat_enabled ? '🛡️ Anti-cheat On' : '⚠️ Anti-cheat Off'}
                                        </p>
                                    {/if}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Server details -->
                <div class="detail-grid">
                    <!-- Description and game info -->
                    <div class="glass-card card-content">
                        <h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center text-shadow">
                            📋 Server Information
                        </h3>
                        
                        {#if liveInfo.description}
                            <div class="info-section">
                                <h4>📝 Description</h4>
                                <div class="info-content">
                                    {#if server.game === 'minecraft'}
                                        <MinecraftMOTD motd={liveInfo.description} />
                                    {:else}
                                        {liveInfo.description}
                                    {/if}
                                </div>
                            </div>
                        {/if}

                        {#if liveInfo.game_mode}
                            <div class="info-section">
                                <h4>🎮 Game Mode</h4>
                                <p class="info-content large-text">{liveInfo.game_mode}</p>
                            </div>
                        {/if}

                        {#if liveInfo.map_name}
                            <div class="info-section">
                                <h4>🗺️ Current Map</h4>
                                <p class="info-content large-text">{liveInfo.map_name}</p>
                            </div>
                        {/if}
                    </div>

                    <!-- Players online -->
                    {#if liveInfo.player_list && liveInfo.player_list.length > 0}
                        <div class="glass-card card-content">
                            <h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center text-shadow">
                                👥 Players Online ({liveInfo.player_list.length})
                            </h3>
                            <div class="players-list">
                                {#each liveInfo.player_list as player}
                                    <div class="player-item">
                                        <div class="player-avatar">
                                            {player.charAt(0).toUpperCase()}
                                        </div>
                                        <span class="player-name">{player}</span>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    {:else}
                        <div class="glass-card card-content">
                            <h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center text-shadow">
                                👥 Players Online
                            </h3>
                            <div class="empty-players">
                                <div class="empty-players-icon">😴</div>
                                <p class="empty-players-text">No players currently online</p>
                            </div>
                        </div>
                    {/if}
                </div>

                <!-- Mods section -->
                {#if liveInfo.mods && liveInfo.mods.length > 0}
                    <div class="glass-card card-content">
                        <h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center text-shadow">
                            🔧 Installed Mods ({liveInfo.mods.length})
                        </h3>
                        <div class="mods-grid">
                            {#each liveInfo.mods as mod}
                                <div class="mod-item">
                                    <p class="mod-name">{mod.name || 'Unknown Mod'}</p>
                                    {#if mod.version}
                                        <p class="mod-version">v{mod.version}</p>
                                    {/if}
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}

                <!-- Error message -->
                {#if liveInfo.error_message}
                    <div class="error-section">
                        <h3 class="error-title">
                            ⚠️ Connection Error
                        </h3>
                        <p class="error-message">{liveInfo.error_message}</p>
                    </div>
                {/if}

                <!-- Auto-refresh indicator -->
                <div class="auto-refresh-indicator">
                    <div class="refresh-badge">
                        <span class="refresh-icon">🔄</span>
                        <span class="refresh-text">Auto-refreshing every 30 seconds</span>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>
