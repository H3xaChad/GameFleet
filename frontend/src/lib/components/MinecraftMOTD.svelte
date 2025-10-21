<script lang="ts">
    import parse from '@sfirew/minecraft-motd-parser'
    
    interface Props {
        motd: string
        className?: string
    }
    
    let { motd, className = '' }: Props = $props()
    
    // Function to parse MOTD
    function getParsedMOTD(motdText: string): string {
        try {
            return parse.textToHTML(motdText)
        } catch (error) {
            console.warn('Failed to parse Minecraft MOTD:', error)
            // Fallback to plain text with basic color code removal
            return motdText.replace(/§[0-9a-fk-or]/gi, '')
        }
    }
    
    // Parse the MOTD to HTML using $derived
    const parsedMOTD = $derived(getParsedMOTD(motd))
</script>

<div class="minecraft-motd {className}">
    {@html parsedMOTD}
</div>

<style>
    .minecraft-motd {
        font-family: 'Courier New', monospace;
        line-height: 1.4;
        white-space: pre-wrap;
        word-break: break-word;
    }
    
    /* Style the parsed Minecraft color codes */
    .minecraft-motd :global(.minecraft-formatted) {
        font-weight: inherit;
    }
    
    /* Ensure text doesn't overflow */
    .minecraft-motd :global(*) {
        max-width: 100%;
        word-wrap: break-word;
    }
</style>