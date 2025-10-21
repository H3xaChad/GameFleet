<script lang="ts">
    interface Props {
        icon: string
        title: string
        value: string | number
        subtitle?: string
        bgColor?: string
    }

    let { icon, title, value, subtitle, bgColor = 'from-game-primary-100 to-game-primary-200' }: Props = $props()
</script>

<div class="glass-card rounded-2xl shadow-game border border-white/50 p-6 hover:shadow-game-lg transition-game transform hover:-translate-y-1 hover:scale-105 game-card">
    <div class="flex items-center">
        <div class={`p-4 bg-gradient-to-br ${bgColor} rounded-xl shadow-game-inner`}>
            <span class="text-2xl">{icon}</span>
        </div>
        <div class="ml-4">
            <p class="text-sm font-semibold text-slate-600 uppercase tracking-wide">{title}</p>
            <p class="text-3xl font-bold text-slate-900 text-shadow">
                {value}
                {#if subtitle}
                    <span class="text-xl text-slate-500">{subtitle}</span>
                {/if}
            </p>
        </div>
    </div>
</div>