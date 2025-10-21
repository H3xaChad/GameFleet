<script lang="ts">
    import { api } from '$lib/api/ApiService'
    import type { GameServer, BaseServerInfo, ServerStatus } from '$lib/api/Api'
    import { onMount } from 'svelte'
    import ServerCard from '$lib/components/ServerCard.svelte'
    import LoadingSpinner from '$lib/components/LoadingSpinner.svelte'
    import ThemeToggle from '$lib/components/ThemeToggle.svelte'

    let gameServers: GameServer[] = []
    let serverLiveInfo: Record<string, BaseServerInfo> = {}
    let loading = true

    onMount(async () => {
        try {
            const response = await api.getServers()
            gameServers = response.data as GameServer[]
            
            // Fetch live info for all servers
            for (const server of gameServers) {
                if (server.id) {
                    try {
                        const liveResponse = await api.serverId.getServerLiveInfoById(server.id)
                        serverLiveInfo[server.id] = liveResponse.data
                    } catch (error) {
                        console.error(`Failed to fetch live info for server ${server.id}:`, error)
                        serverLiveInfo[server.id] = {
                            status: 'unknown' as ServerStatus,
                            error_message: 'Failed to fetch live information'
                        }
                    }
                }
            }
        } catch (error) {
            console.error('Failed to fetch servers:', error)
        } finally {
            loading = false
        }
    })

    function navigateToServer(serverId: string) {
        window.location.href = `/server/${serverId}`
    }
</script>

<div class="page-container">
    <!-- Background pattern -->
    <div class="background-pattern"></div>
    
    <div class="page-content">
        <!-- Header -->
        <div class="page-header">
            <div class="header-controls">
                <ThemeToggle />
            </div>
            <h1 class="page-title">
                🎮 Game Server Dashboard
            </h1>
            <p class="page-subtitle">Monitor and manage all your game servers in one place</p>
            <div class="header-badge">
                <span>🚀 Real-time monitoring</span>
            </div>
        </div>

        <!-- Loading state -->
        {#if loading}
            <div class="loading-container">
                <LoadingSpinner size="lg" message="🔍 Discovering servers..." />
            </div>
        {:else if gameServers.length === 0}
            <!-- Empty state -->
            <div class="empty-state">
                <div class="empty-state-icon">🏗️</div>
                <h3 class="empty-state-title">Ready to get started?</h3>
                <p class="empty-state-description">Add your first game server and start monitoring its performance in real-time</p>
                <button class="btn-game">
                    ➕ Add Your First Server
                </button>
            </div>
        {:else}
            <!-- Server grid -->
            <div class="server-grid">
                {#each gameServers as server}
                    <ServerCard 
                        {server} 
                        liveInfo={serverLiveInfo[server.id || '']} 
                        onClick={navigateToServer}
                    />
                {/each}
            </div>

            <!-- Stats summary -->
            <div class="stats-container">
                <h2 class="stats-title">
                    📊 Server Overview
                </h2>
                <div class="stats-grid">
                    <div class="stat-card total">
                        <div class="stat-value total">{gameServers.length}</div>
                        <div class="stat-label">🏢 Total Servers</div>
                    </div>
                    <div class="stat-card online">
                        <div class="stat-value online">
                            {Object.values(serverLiveInfo).filter(info => info.status === 'online').length}
                        </div>
                        <div class="stat-label">🟢 Online</div>
                    </div>
                    <div class="stat-card offline">
                        <div class="stat-value offline">
                            {Object.values(serverLiveInfo).filter(info => info.status === 'offline').length}
                        </div>
                        <div class="stat-label">🔴 Offline</div>
                    </div>
                    <div class="stat-card players">
                        <div class="stat-value players">
                            {Object.values(serverLiveInfo).reduce((total, info) => total + (info.players_online || 0), 0)}
                        </div>
                        <div class="stat-label">👥 Total Players</div>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>