#!/usr/bin/env bash

BASE_DOWNLOAD_PATH="$(pwd)/../../data/smogon_data/"
SMOGUN_URL="https://www.smogon.com/stats/"

months=("07" "08" "09" "10")
tiers=("ubers" "ou" "uu" "ru" "nu" "pu" "zu")
elos_all=("0" "1500" "1630" "1760") # valid for all tiers except OU
elos_ou=("0" "1500" "1695" "1825") # valid for OU

mkdir -p "$BASE_DOWNLOAD_PATH"

for m in "${months[@]}"; do

    # Create year/month directory
    DOWNLOAD_PATH="${BASE_DOWNLOAD_PATH}/${m}"
    mkdir -p "$DOWNLOAD_PATH"

    for t in "${tiers[@]}"; do

        # Choose the correct set of elos based on the tier
        if [ "$t" == "ou" ]; then
            elos=("${elos_ou[@]}")
        else
            elos=("${elos_all[@]}")
        fi

        for e in "${elos[@]}"; do

            url=$(printf "%s2025-%s/chaos/gen9%s-%s.json" \
                "$SMOGUN_URL" \
                "$m" \
                "$t" \
                "$e"
            )

            echo "Downloading: $url"

            if wget -q --show-progress -P "$DOWNLOAD_PATH" "$url"; then
                echo "  ✓ Success"
            else
                echo "  ✗ Not found, skipping"
            fi

        done
    done
done
