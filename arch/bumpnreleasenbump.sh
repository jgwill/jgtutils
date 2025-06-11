. release-n-test.sh && sleep 16 && (cdjgtfxcon && . bump_jgtutils.sh && make dev-release-plus && cdjgtpy && . bump_jgtutils.sh;make dev-release-plus && sleep 22 && cdjgtml && . bump_jgtpy.sh && make dev-release-plus)

