<script lang="ts">
    interface Props {
        icon: string
        title: string
        value: string | number
        subtitle?: string
        bgColor?: 'primary' | 'secondary' | 'accent' | 'warning'
        type?: 'default' | 'version'
    }

    let { icon, title, value, subtitle, bgColor = 'primary', type = 'default' }: Props = $props()
</script>

<div class="glass-card server-card">
    <div class="stat-card-component">
        <div class="stat-icon {bgColor}">
            <span>{icon}</span>
        </div>
        <div class="stat-info">
            <p class="stat-title">{title}</p>
            <p class="stat-main-value {type === 'version' ? 'version' : ''}">
                {value}
                {#if subtitle}
                    <span class="stat-subtitle">{subtitle}</span>
                {/if}
            </p>
        </div>
    </div>
</div>