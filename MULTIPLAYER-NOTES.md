# Survival World — multiplayer and competitive systems status

## Implemented in the current browser prototype

- Local survival-time and resource records stored in browser `localStorage`.
- A timed 3-minute survival challenge and a 60-second resource gathering contest.
- A practice duel against a zombie target.
- XP and level progression; outfit color variants unlock at levels 3 and 5.
- Client-side score tracking and save/load.

These are local prototype features. They are not shared between players or devices and can be edited by a player because the browser owns the state.

## Not implemented yet

- Real accounts, matchmaking, lobbies, party invites or online sessions.
- Player-versus-player networking and server-side hit validation.
- Global leaderboards, ranked seasons, tournaments and cross-device rewards.
- Authoritative anti-cheat, server persistence, moderation and reporting.

## Required direction for true multiplayer

1. Keep the browser as a rendering/input client only; do not trust client-submitted inventory, XP, health, movement, kills or match results.
2. Add an authoritative server (for example, Node.js/TypeScript) with WebSocket sessions, authentication, matchmaking and rate limits.
3. Simulate or validate movement, zombie AI, combat cooldowns, damage, crafting costs, resource collection and match timers on the server.
4. Persist player profiles, inventories, seasons, tournament brackets and leaderboard results in a database.
5. Send snapshots/deltas to clients and interpolate remote players; reconcile the local player against server state.
6. Add server-side audit logs, anomaly detection, replayable match events and server-issued rewards.
7. Add PvP only after latency compensation, spawn protection, team/ranked rules and anti-grief controls are tested.

No multiplayer server, credentials, database or hosting service is configured by this prototype. Hosting the static GitHub Pages page does not provide a game server.
