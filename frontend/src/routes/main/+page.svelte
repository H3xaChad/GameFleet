<script lang="ts">
    import { api } from '$lib/api/ApiService'
    import type { GameServer, BaseServerInfo, ServerStatus } from '$lib/api/Api'
    import { onMount } from 'svelte'
    import ServerCard from '$lib/components/ServerCard.svelte'
    import LoadingSpinner from '$lib/components/LoadingSpinner.svelte'

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
            <div class="py-20">
                <LoadingSpinner size="lg" message="🔍 Discovering servers..." />
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
                    <ServerCard 
                        {server} 
                        liveInfo={serverLiveInfo[server.id || '']} 
                        onClick={navigateToServer}
                    />
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
</style>