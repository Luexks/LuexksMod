    if (thisBlock->sb.getFutureFeatures()&Block::TURRET)
    {
        muzzleOffset = thisBlock->sb.bt->barrelSize;
        const bool calcSize = muzzleOffset == f2();
        if (calcSize)
        {
            muzzleOffset.x = thisBlock->spec->radius * (boostedStats.muzzleVel / 800.f);
            muzzleOffset.y = 1.1f * getProjectileSize();
        }

        const float turretMaxRad = 0.9f * thisBlock->spec->minradius;
        const float barrelWidth  = 1.5f * muzzleOffset.y;
        turretBarrelCount = thisBlock->sb.bt->barrelCount;
        if (!turretBarrelCount)
        {
            turretBarrelCount = max(1, round_int(boostedStats.roundsPerSec / 4.f));
            while (turretBarrelCount > 1 && turretBarrelCount * barrelWidth > turretMaxRad) {
                turretBarrelCount--;
            }
        }

        turretRadius = min(1.5f * turretBarrelCount * barrelWidth, turretMaxRad);
        if (calcSize)
        {
            muzzleOffset.y = min(muzzleOffset.y, 0.7f * turretRadius);
            muzzleOffset.x = max(muzzleOffset.x, 1.75f * turretRadius);
        }
    }

static float projectileSize(const SerialCannon& sc, float charge)
{
    float size = sc.projectileSize;
    if (size <= 0.f) {
        float dmg = sc.damage;
        if (sc.explosive&kExplodeFlags)
            dmg *= max(2.f, (sc.explodeRadius / kComponentWidth));
        size = max(0.25f * sqrt(dmg), 0.75f);
    }
    return max(1.f, size * sqrt(charge));
}