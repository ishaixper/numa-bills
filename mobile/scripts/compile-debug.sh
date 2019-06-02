#!/usr/bin/env bash
set -xeuo pipefail
dos2unix ./gradlew
#./gradlew clean
./gradlew assembleDebug