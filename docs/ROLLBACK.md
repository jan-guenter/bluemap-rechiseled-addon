# Rollback

This add-on stores no world, block, entity, NBT, registry, network, or client
state. To roll back, remove its JAR from BlueMap's add-on directory and restart
BlueMap/the server. All 3,627 Rechiseled IDs then use stock BlueMap rendering.

For a live diagnostic rollback without removing the JAR, add
`rechiseled-fusion-1.2.5-1.3.12` to
`bluemap.rechiseled.disabledProfiles` (or
`BLUEMAP_RECHISELED_DISABLED_PROFILES`) and restart. This disables exactly the
1,743-ID route.

A per-block malformed observation already resets partial geometry/color and
uses the original stock blockstate. Capacity exhaustion still propagates and is
not a rollback event.
