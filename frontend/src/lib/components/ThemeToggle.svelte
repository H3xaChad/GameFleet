<script lang="ts">
    import { onMount } from 'svelte'
    
    let isDark = $state(false)
    
    // Initialize theme from localStorage or system preference
    onMount(() => {
        const stored = localStorage.getItem('theme')
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches
        
        isDark = stored === 'dark' || (!stored && prefersDark)
        updateTheme()
        
        // Listen for system theme changes
        const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
        const handleChange = (e: MediaQueryListEvent) => {
            if (!localStorage.getItem('theme')) {
                isDark = e.matches
                updateTheme()
            }
        }
        
        mediaQuery.addEventListener('change', handleChange)
        return () => mediaQuery.removeEventListener('change', handleChange)
    })
    
    function updateTheme() {
        const root = document.documentElement
        if (isDark) {
            root.setAttribute('data-theme', 'dark')
            localStorage.setItem('theme', 'dark')
        } else {
            root.removeAttribute('data-theme')
            localStorage.setItem('theme', 'light')
        }
    }
    
    function toggleTheme() {
        isDark = !isDark
        updateTheme()
    }
</script>

<button
    class="theme-toggle"
    onclick={toggleTheme}
    aria-label="Toggle dark mode"
    title={isDark ? 'Switch to light mode' : 'Switch to dark mode'}
>
    <div class="toggle-container">
        <div class="toggle-slider" class:dark={isDark}>
            <span class="toggle-icon">
                {#if isDark}
                    🌙
                {:else}
                    ☀️
                {/if}
            </span>
        </div>
    </div>
</button>

<style>
    .theme-toggle {
        position: relative;
        background: none;
        border: none;
        cursor: pointer;
        padding: 0;
        outline: none;
    }
    
    .toggle-container {
        width: 3.5rem;
        height: 2rem;
        background: var(--glass-bg);
        border: 2px solid var(--border-secondary);
        border-radius: 9999px;
        position: relative;
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .theme-toggle:hover .toggle-container {
        transform: scale(1.05);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    }
    
    .toggle-slider {
        position: absolute;
        top: 2px;
        left: 2px;
        width: 1.5rem;
        height: 1.5rem;
        background: var(--bg-primary);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .toggle-slider.dark {
        transform: translateX(1.5rem);
    }
    
    .toggle-icon {
        font-size: 0.875rem;
        line-height: 1;
    }
    
    .theme-toggle:focus-visible .toggle-container {
        outline: 2px solid var(--status-online);
        outline-offset: 2px;
    }
</style>