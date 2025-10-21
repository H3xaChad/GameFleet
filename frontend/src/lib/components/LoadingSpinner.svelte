<script lang="ts">
    interface Props {
        size?: 'sm' | 'md' | 'lg' | 'xl'
        message?: string
        color?: 'primary' | 'secondary' | 'accent'
    }

    let { size = 'md', message, color = 'primary' }: Props = $props()

    const sizeClasses = {
        sm: 'h-8 w-8',
        md: 'h-16 w-16',
        lg: 'h-20 w-20',
        xl: 'h-24 w-24'
    }

    const colorClasses = {
        primary: {
            border: 'border-game-primary-200',
            borderTop: 'border-t-game-primary-600'
        },
        secondary: {
            border: 'border-game-secondary-200',
            borderTop: 'border-t-game-secondary-600'
        },
        accent: {
            border: 'border-game-accent-200',
            borderTop: 'border-t-game-accent-600'
        }
    }

    const textSizeClasses = {
        sm: 'text-sm',
        md: 'text-lg',
        lg: 'text-xl',
        xl: 'text-2xl'
    }
</script>

<div class="flex items-center justify-center">
    <div class="relative loading-spinner">
        <div class={`animate-spin rounded-full border-4 ${sizeClasses[size]} ${colorClasses[color].border}`}></div>
        <div class={`animate-spin rounded-full border-4 absolute top-0 ${sizeClasses[size]} ${colorClasses[color].borderTop}`}></div>
    </div>
    {#if message}
        <span class={`ml-4 text-slate-700 font-medium text-shadow ${textSizeClasses[size]}`}>
            {message}
        </span>
    {/if}
</div>