# GameFleet

Simple dashboard to keep track of your game servers. Shows who's online and if servers are running.

## What it does

- Monitor different game servers in one place
- See player counts and server status at real-time
- Displays all fetchable server info like ping, player count (current/max), description, server icon, etc.
- Web interface that updates automatically
- Easy to run with Docker

## Setup

You'll need Docker installed.

1. **Get the code**
   ```bash
   git clone https://github.com/H3xaChad/GameFleet.git
   cd GameFleet
   ```

2. **Set up config**
   ```bash
   cp .env.example .env
   # Edit .env with your database info
   ```

3. **Run it**
   ```bash
   make up
   ```

4. **Open in browser**
   - Main app: http://localhost:3000
   - API: http://localhost:8000

## Development

### Running locally

**Backend:**
```bash
cd backend
make dev
```

**Frontend:**
```bash
cd frontend
pnpm dev
```

### Building with Docker

**Development mode:**
```bash
make dev
```

**Production mode:**
```bash
make up
```

### Deployment

To deploy the existing Docker image (when available):
```bash
docker pull h3xachad/gamefleet-backend:latest
docker pull h3xachad/gamefleet-frontend:latest
# Then use your preferred orchestration method (docker-compose, k8s, etc.)
```

## Commands

```bash
make dev     # Development mode
make up      # Production mode  
make down    # Stop everything
make logs    # See logs
make clean   # Clean up
```

## Supported Games

Works with:
- Minecraft Java Edition
- Satisfactory

Working on:
- Minecraft Bedrock
- Factorio
- ARK

## Config

Main settings in `.env`:

| Setting | What it does |
|---------|--------------|
| `DB_HOST` | Where your database is |
| `DB_PASSWORD` | Database password |
| `BACKEND_PORT` | API port (default 8000) |
| `FRONTEND_PORT` | Web port (default 3000) |

## License

MIT License - do whatever you want with it.
