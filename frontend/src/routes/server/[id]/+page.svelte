<script lang="ts">
    import { page } from '$app/state'
    import { api } from '$lib/api/ApiService'
    import type { GameServer, BaseServerInfo, ServerStatus } from '$lib/api/Api'
    import { onMount, onDestroy } from 'svelte'
    import StatusBadge from '$lib/components/StatusBadge.svelte'
    import LoadingSpinner from '$lib/components/LoadingSpinner.svelte'
    import StatCard from '$lib/components/StatCard.svelte'

    let server: GameServer | null = null
    let liveInfo: BaseServerInfo | null = null
    let loading = true
    let error: string | null = null
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

    function formatUptime(seconds: number): string {
        const days = Math.floor(seconds / (24 * 3600))
        const hours = Math.floor((seconds % (24 * 3600)) / 3600)
        const minutes = Math.floor((seconds % 3600) / 60)
        
        if (days > 0) return `${days}d ${hours}h ${minutes}m`
        if (hours > 0) return `${hours}h ${minutes}m`
        return `${minutes}m`
    }
</script>

<svelte:head>
    <title>{server ? server.name : 'Server Details'} - Game Server Dashboard</title>
</svelte:head>

<div class="min-h-screen bg-gradient-to-br from-game-primary-50 via-white to-game-secondary-50 relative">
    <!-- Background pattern -->
    <div class="absolute inset-0 gaming-pattern opacity-30 pointer-events-none"></div>
    
    <!-- Header -->
    <div class="glass-card shadow-game-lg border-b border-white/30 relative z-10">
        <div class="max-w-7xl mx-auto px-8 py-6">
            <div class="flex items-center">
                <button 
                    on:click={goBack}
                    class="mr-6 p-3 hover:bg-game-primary-100 rounded-xl transition-game transform hover:scale-105 btn-game"
                    aria-label="Go back"
                    title="Go back"
                >
                    <span class="text-xl font-semibold text-shadow">← Back</span>
                </button>
                <h1 class="text-3xl font-bold bg-gradient-to-r from-game-primary-600 to-game-secondary-600 bg-clip-text text-transparent text-shadow">
                    🎮 Server Details
                </h1>
            </div>
        </div>
    </div>

    <div class="max-w-7xl mx-auto p-8">
        {#if loading}
            <!-- Loading state -->
            <div class="py-20">
                <LoadingSpinner size="md" message="🔍 Loading server information..." />
            </div>
        {:else if error}
            <!-- Error state -->
            <div class="text-center py-20">
                <div class="text-6xl mb-4">😕</div>
                <h3 class="text-2xl font-bold text-slate-800 mb-3">Oops! Something went wrong</h3>
                <p class="text-slate-600 mb-8 text-lg">{error}</p>
                <button 
                    on:click={goBack}
                    class="bg-gradient-to-r from-game-primary-600 to-game-secondary-600 hover:from-game-primary-700 hover:to-game-secondary-700 text-white px-8 py-4 rounded-xl font-semibold transition-game transform hover:scale-105 shadow-game-lg btn-game"
                >
                    🏠 Go Back Home
                </button>
            </div>
        {:else if server && liveInfo}
            <!-- Server information -->
            <div class="space-y-8">
                <!-- Server header -->
                <div class="glass-card rounded-2xl shadow-game-xl border border-white/50 p-8 hover:shadow-game-xl transition-game game-card">
                    <div class="flex items-start justify-between">
                        <div>
                            <h2 class="text-4xl font-bold text-slate-800 mb-2 text-shadow">{server.name}</h2>
                            <p class="text-slate-600 capitalize text-xl mb-2 font-medium">🎯 {server.game.replace('_', ' ')}</p>
                            <p class="text-slate-500 text-lg font-mono">🌐 {server.address}:{server.port}</p>
                        </div>
                        
                        <!-- Status badge -->
                        <div class="flex items-center">
                            <StatusBadge status={liveInfo.status} />
                        </div>
                    </div>
                </div>

                <!-- Server stats grid -->
                <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                    <!-- Players -->
                    <StatCard
                        icon="👥"
                        title="Players"
                        value={liveInfo.players_online ?? 'N/A'}
                        subtitle={liveInfo.players_max ? `/ ${liveInfo.players_max}` : undefined}
                        bgColor="from-game-primary-100 to-game-primary-200"
                    />

                    <!-- Latency -->
                    {#if liveInfo.latency !== null}
                        <StatCard
                            icon="⚡"
                            title="Latency"
                            value={`${liveInfo.latency}ms`}
                            bgColor="from-game-accent-100 to-game-accent-200"
                        />
                    {/if}

                    <!-- Version -->
                    {#if liveInfo.version}
                        <StatCard
                            icon="🔧"
                            title="Version"
                            value={liveInfo.version}
                            bgColor="from-game-secondary-100 to-game-secondary-200"
                        />
                    {/if}

                    <!-- Security info -->
                    <div class="glass-card rounded-2xl shadow-game border border-white/50 p-6 hover:shadow-game-lg transition-game transform hover:-translate-y-1 hover:scale-105 game-card">
                        <div class="flex items-center">
                            <div class="p-4 bg-gradient-to-br from-game-warning-100 to-game-error-100 rounded-xl shadow-game-inner">
                                <span class="text-2xl">🔒</span>
                            </div>
                            <div class="ml-4">
                                <p class="text-sm font-semibold text-slate-600 uppercase tracking-wide">Security</p>
                                <div class="space-y-1">
                                    {#if liveInfo.password_protected !== null}
                                        <p class="text-sm text-slate-700 font-medium">
                                            {liveInfo.password_protected ? '🔐 Password Required' : '🔓 No Password'}
                                        </p>
                                    {/if}
                                    {#if liveInfo.anti_cheat_enabled !== null}
                                        <p class="text-sm text-slate-700 font-medium">
                                            {liveInfo.anti_cheat_enabled ? '🛡️ Anti-cheat On' : '⚠️ Anti-cheat Off'}
                                        </p>
                                    {/if}
                                </div>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Server details -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
                    <!-- Description and game info -->
                    <div class="glass-card rounded-2xl shadow-game border border-white/50 p-8 hover:shadow-game-lg transition-game game-card">
                        <h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center text-shadow">
                            📋 Server Information
                        </h3>
                        
                        {#if liveInfo.description}
                            <div class="mb-6">
                                <h4 class="text-sm font-bold text-slate-600 mb-3 uppercase tracking-wide">📝 Description</h4>
                                <p class="text-slate-700 bg-gradient-to-r from-slate-50 to-slate-100 p-4 rounded-xl border border-slate-200 backdrop-blur-game">{liveInfo.description}</p>
                            </div>
                        {/if}

                        {#if liveInfo.game_mode}
                            <div class="mb-6">
                                <h4 class="text-sm font-bold text-slate-600 mb-3 uppercase tracking-wide">🎮 Game Mode</h4>
                                <p class="text-slate-700 text-lg font-medium text-shadow">{liveInfo.game_mode}</p>
                            </div>
                        {/if}

                        {#if liveInfo.map_name}
                            <div class="mb-6">
                                <h4 class="text-sm font-bold text-slate-600 mb-3 uppercase tracking-wide">🗺️ Current Map</h4>
                                <p class="text-slate-700 text-lg font-medium text-shadow">{liveInfo.map_name}</p>
                            </div>
                        {/if}
                    </div>

                    <!-- Players online -->
                    {#if liveInfo.player_list && liveInfo.player_list.length > 0}
                        <div class="glass-card rounded-2xl shadow-game border border-white/50 p-8 hover:shadow-game-lg transition-game game-card">
                            <h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center text-shadow">
                                👥 Players Online ({liveInfo.player_list.length})
                            </h3>
                            <div class="space-y-3 max-h-72 overflow-y-auto custom-scrollbar">
                                {#each liveInfo.player_list as player}
                                    <div class="flex items-center p-3 bg-gradient-to-r from-game-primary-50 to-game-secondary-50 rounded-xl border border-game-primary-100 hover:from-game-primary-100 hover:to-game-secondary-100 transition-game">
                                        <div class="w-10 h-10 bg-gradient-to-br from-game-primary-500 to-game-secondary-500 rounded-full flex items-center justify-center text-white text-sm font-bold mr-4 shadow-game">
                                            {player.charAt(0).toUpperCase()}
                                        </div>
                                        <span class="text-slate-700 font-medium text-shadow">{player}</span>
                                    </div>
                                {/each}
                            </div>
                        </div>
                    {:else}
                        <div class="glass-card rounded-2xl shadow-game border border-white/50 p-8 hover:shadow-game-lg transition-game game-card">
                            <h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center text-shadow">
                                👥 Players Online
                            </h3>
                            <div class="text-center py-12">
                                <div class="text-4xl mb-4 animate-float">😴</div>
                                <p class="text-slate-500 text-lg">No players currently online</p>
                            </div>
                        </div>
                    {/if}
                </div>

                <!-- Mods section -->
                {#if liveInfo.mods && liveInfo.mods.length > 0}
                    <div class="glass-card rounded-2xl shadow-game border border-white/50 p-8 hover:shadow-game-lg transition-game game-card">
                        <h3 class="text-xl font-bold text-slate-800 mb-6 flex items-center text-shadow">
                            🔧 Installed Mods ({liveInfo.mods.length})
                        </h3>
                        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                            {#each liveInfo.mods as mod}
                                <div class="p-4 bg-gradient-to-br from-slate-50 to-slate-100 rounded-xl border border-slate-200 hover:shadow-game transition-game transform hover:scale-105 backdrop-blur-game">
                                    <p class="font-semibold text-slate-800 text-shadow">{mod.name || 'Unknown Mod'}</p>
                                    {#if mod.version}
                                        <p class="text-sm text-slate-600 mt-1">v{mod.version}</p>
                                    {/if}
                                </div>
                            {/each}
                        </div>
                    </div>
                {/if}

                <!-- Error message -->
                {#if liveInfo.error_message}
                    <div class="bg-gradient-to-r from-game-error-50 to-game-error-100 border border-game-error-200 rounded-2xl p-8 shadow-game">
                        <h3 class="text-xl font-bold text-game-error-800 mb-3 flex items-center text-shadow">
                            ⚠️ Connection Error
                        </h3>
                        <p class="text-game-error-700 text-lg">{liveInfo.error_message}</p>
                    </div>
                {/if}

                <!-- Auto-refresh indicator -->
                <div class="text-center">
                    <div class="inline-flex items-center px-6 py-3 glass-card rounded-full shadow-game border border-white/50">
                        <span class="mr-3 animate-spin text-game-primary-600">🔄</span>
                        <span class="text-slate-600 font-medium">Auto-refreshing every 30 seconds</span>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .custom-scrollbar::-webkit-scrollbar {
        width: 8px;
    }
    .custom-scrollbar::-webkit-scrollbar-track {
        background: linear-gradient(135deg, #f1f5f9, #e2e8f0);
        border-radius: 4px;
    }
    .custom-scrollbar::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #667eea, #764ba2);
        border-radius: 4px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    .custom-scrollbar::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #5a6fd8, #6a42a0);
    }

    .gaming-pattern {
        background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,0.15) 1px, transparent 0);
        background-size: 20px 20px;
    }

    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }

    .animate-float {
        animation: float 3s ease-in-out infinite;
    }
</style>