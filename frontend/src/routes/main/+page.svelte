<script lang="ts">
    import { api } from '$lib/api/ApiService'
    import type { GameServer, BaseServerInfo, ServerStatus } from '$lib/api/Api'
    import { onMount } from 'svelte'

    let gameServers: GameServer[] = []
    let serverLiveInfo: Record<string, BaseServerInfo> = {}
    let loading = true

    const statusColors: Record<ServerStatus, string> = {
        online: 'text-game-accent-600',
        offline: 'text-game-error-600',
        unknown: 'text-game-warning-600'
    }

    const statusBgColors: Record<ServerStatus, string> = {
        online: 'bg-gradient-to-r from-game-accent-100 to-game-accent-200 border-game-accent-200',
        offline: 'bg-gradient-to-r from-game-error-100 to-game-error-200 border-game-error-200',
        unknown: 'bg-gradient-to-r from-game-warning-100 to-game-warning-200 border-game-warning-200'
    }

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

<div class="min-h-screen bg-gradient-to-br from-game-primary-50 via-white to-game-secondary-50 p-8 relative">
    <!-- Background pattern -->
    <div class="absolute inset-0 gaming-pattern opacity-20 pointer-events-none"></div>
    
    <div class="max-w-7xl mx-auto relative z-10">
        <!-- Header -->
        <div class="mb-12 text-center">
            <h1 class="text-6xl font-bold bg-gradient-to-r from-game-primary-600 via-game-secondary-600 to-game-accent-600 bg-clip-text text-transparent mb-4 text-shadow">
                🎮 Game Server Dashboard
            </h1>
            <p class="text-slate-600 text-xl font-medium">Monitor and manage all your game servers in one place</p>
            <div class="mt-6 flex justify-center">
                <div class="glass-card rounded-full px-6 py-3 shadow-game border border-white/50">
                    <span class="text-slate-500 font-medium">🚀 Real-time monitoring</span>
                </div>
            </div>
        </div>

        <!-- Loading state -->
        {#if loading}
            <div class="flex items-center justify-center py-20">
                <div class="relative loading-spinner">
                    <div class="animate-spin rounded-full h-20 w-20 border-4 border-game-primary-200"></div>
                    <div class="animate-spin rounded-full h-20 w-20 border-4 border-t-game-primary-600 absolute top-0"></div>
                </div>
                <span class="ml-6 text-xl text-slate-700 font-semibold text-shadow">🔍 Discovering servers...</span>
            </div>
        {:else if gameServers.length === 0}
            <!-- Empty state -->
            <div class="text-center py-20">
                <div class="text-8xl mb-6">🏗️</div>
                <h3 class="text-3xl font-bold text-slate-800 mb-4">Ready to get started?</h3>
                <p class="text-slate-600 mb-8 text-xl max-w-md mx-auto">Add your first game server and start monitoring its performance in real-time</p>
                <button class="bg-gradient-to-r from-game-primary-600 to-game-secondary-600 hover:from-game-primary-700 hover:to-game-secondary-700 text-white px-8 py-4 rounded-xl font-semibold transition-game transform hover:scale-105 shadow-game-lg text-lg btn-game">
                    ➕ Add Your First Server
                </button>
            </div>
        {:else}
            <!-- Server grid -->
            <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-8 mb-12">
                {#each gameServers as server}
                    {@const liveInfo = serverLiveInfo[server.id || '']}
                    <div 
                        class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-lg border border-white/50 hover:shadow-2xl transition-all duration-300 cursor-pointer transform hover:-translate-y-2 hover:scale-105"
                        on:click={() => server.id && navigateToServer(server.id)}
                        role="button"
                        tabindex="0"
                        on:keypress={(e) => e.key === 'Enter' && server.id && navigateToServer(server.id)}
                    >
                        <!-- Status indicator -->
                        <div class="p-6 pb-4">
                            {#if liveInfo}
                                <div class={`inline-flex items-center px-4 py-2 rounded-full text-sm font-bold border-2 ${statusBgColors[liveInfo.status]} shadow-sm`}>
                                    <div class={`w-3 h-3 rounded-full mr-3 ${liveInfo.status === 'online' ? 'bg-emerald-500 animate-pulse' : liveInfo.status === 'offline' ? 'bg-rose-500' : 'bg-amber-500 animate-pulse'}`}></div>
                                    <span class={statusColors[liveInfo.status]}>
                                        {liveInfo.status === 'online' ? '🟢' : liveInfo.status === 'offline' ? '🔴' : '🟡'} 
                                        {liveInfo.status.charAt(0).toUpperCase() + liveInfo.status.slice(1)}
                                    </span>
                                </div>
                            {:else}
                                <div class="inline-flex items-center px-4 py-2 rounded-full text-sm font-bold border-2 bg-gradient-to-r from-gray-100 to-slate-100 border-gray-200">
                                    <div class="w-3 h-3 rounded-full mr-3 bg-gray-400 animate-pulse"></div>
                                    <span class="text-gray-500">🔍 Checking...</span>
                                </div>
                            {/if}
                        </div>

                        <div class="px-6 pb-6">
                            <!-- Game name and info -->
                            <div class="mb-4">
                                <h3 class="font-bold text-slate-800 text-xl leading-tight mb-2">{server.name}</h3>
                                <p class="text-base text-slate-600 capitalize font-medium">🎯 {server.game.replace('_', ' ')}</p>
                            </div>

                            <!-- Server details -->
                            <div class="space-y-3 text-sm">
                                <div class="flex items-center text-slate-600 bg-slate-50 p-3 rounded-lg">
                                    <span class="mr-3 font-semibold">🌐</span>
                                    <span class="font-mono">{server.address}:{server.port}</span>
                                </div>

                                {#if liveInfo && liveInfo.players_online !== null && liveInfo.players_max !== null}
                                    <div class="flex items-center text-slate-600 bg-slate-50 p-3 rounded-lg">
                                        <span class="mr-3 font-semibold">👥</span>
                                        <span class="font-semibold">{liveInfo.players_online}/{liveInfo.players_max} players</span>
                                    </div>
                                {/if}

                                {#if liveInfo && liveInfo.latency}
                                    <div class="flex items-center text-slate-600 bg-slate-50 p-3 rounded-lg">
                                        <span class="mr-3 font-semibold">⚡</span>
                                        <span class="font-semibold">{liveInfo.latency}ms</span>
                                    </div>
                                {/if}

                                {#if liveInfo && liveInfo.version}
                                    <div class="flex items-center text-slate-600 bg-slate-50 p-3 rounded-lg">
                                        <span class="mr-3 font-semibold">🔧</span>
                                        <span class="font-semibold">v{liveInfo.version}</span>
                                    </div>
                                {/if}
                            </div>

                            <!-- Error message -->
                            {#if liveInfo && liveInfo.error_message}
                                <div class="mt-4 p-3 bg-gradient-to-r from-red-50 to-pink-50 border border-red-200 rounded-lg text-xs text-red-700 font-medium">
                                    ⚠️ {liveInfo.error_message}
                                </div>
                            {/if}
                        </div>
                    </div>
                {/each}
            </div>

            <!-- Stats summary -->
            <div class="bg-white/70 backdrop-blur-sm rounded-2xl shadow-xl border border-white/50 p-8 hover:shadow-2xl transition-all duration-300">
                <h2 class="text-2xl font-bold text-slate-800 mb-8 flex items-center justify-center">
                    📊 Server Overview
                </h2>
                <div class="grid grid-cols-1 md:grid-cols-4 gap-6">
                    <div class="text-center p-6 bg-gradient-to-br from-indigo-50 to-purple-50 rounded-xl border border-indigo-100">
                        <div class="text-4xl font-bold text-indigo-600 mb-2">{gameServers.length}</div>
                        <div class="text-sm text-slate-600 font-semibold uppercase tracking-wide">🏢 Total Servers</div>
                    </div>
                    <div class="text-center p-6 bg-gradient-to-br from-emerald-50 to-teal-50 rounded-xl border border-emerald-100">
                        <div class="text-4xl font-bold text-emerald-600 mb-2">
                            {Object.values(serverLiveInfo).filter(info => info.status === 'online').length}
                        </div>
                        <div class="text-sm text-slate-600 font-semibold uppercase tracking-wide">🟢 Online</div>
                    </div>
                    <div class="text-center p-6 bg-gradient-to-br from-rose-50 to-pink-50 rounded-xl border border-rose-100">
                        <div class="text-4xl font-bold text-rose-600 mb-2">
                            {Object.values(serverLiveInfo).filter(info => info.status === 'offline').length}
                        </div>
                        <div class="text-sm text-slate-600 font-semibold uppercase tracking-wide">🔴 Offline</div>
                    </div>
                    <div class="text-center p-6 bg-gradient-to-br from-amber-50 to-orange-50 rounded-xl border border-amber-100">
                        <div class="text-4xl font-bold text-amber-600 mb-2">
                            {Object.values(serverLiveInfo).reduce((total, info) => total + (info.players_online || 0), 0)}
                        </div>
                        <div class="text-sm text-slate-600 font-semibold uppercase tracking-wide">👥 Total Players</div>
                    </div>
                </div>
            </div>
        {/if}
    </div>
</div>

<style>
    .gaming-pattern {
        background-image: radial-gradient(circle at 1px 1px, rgba(255,255,255,0.15) 1px, transparent 0);
        background-size: 20px 20px;
    }

    .loading-spinner {
        position: relative;
    }

    .loading-spinner::after {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        border-radius: 50%;
        background: conic-gradient(transparent, rgba(99, 102, 241, 0.4), transparent);
        animation: spin 2s linear infinite;
    }
</style>