<script lang="ts">
    import { api } from '$lib/api/ApiService'
    import type { GameServer } from '$lib/api/Api'

    let gameServers: GameServer[] = []

    api.api.getServersApiServersGet().then((response) => {
        gameServers = response.data as GameServer[]
        console.log('Servers from API:', gameServers)
    })

</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://svelte.dev/docs/kit">svelte.dev/docs/kit</a> to read the documentation</p>

<p>Basic Server Info:</p>
{#if gameServers.length > 0}
    <ul>
        {#each gameServers as server}
            <li>
                <strong>{server.id}</strong> - {server.game} - {server.name} - {server.address}:{server.port}
            </li>
        {/each}
    </ul>
{:else}
    <p>Loading servers...</p>
{/if}