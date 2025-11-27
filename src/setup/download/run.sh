#!/usr/bin/env bash

BASE_DOWNLOAD_PATH="$(pwd)/../../data/smogon_data/"
SMOGUN_URL="https://www.smogon.com/stats/"

years=("2022" "2023" "2024" "2025")
months=("01" "02" "03" "04" "05" "06" "07" "08" "09" "10" "11" "12")
tiers=("ubers" "ou" "uu" "ru" "nu" "pu" "zu")
elos_all=("0" "1500" "1630" "1760") # valid for all tiers except OU
elos_ou=("0" "1500" "1695" "1825") # valid for OU

mkdir -p "$BASE_DOWNLOAD_PATH"

for y in "${years[@]}"; do

    # Determine valid months for this year
    if [ "$y" -eq 2022 ]; then
        valid_months=("11" "12")
    elif [ "$y" -eq 2025 ]; then
        valid_months=("01" "02" "03" "04" "05" "06" "07" "08" "09" "10")
    else
        valid_months=("${months[@]}")
    fi

    for m in "${valid_months[@]}"; do

        # Create year/month directory
        DOWNLOAD_PATH="${BASE_DOWNLOAD_PATH}/${y}/${m}"
        mkdir -p "$DOWNLOAD_PATH"

        for t in "${tiers[@]}"; do

            # Choose the correct set of elos based on the tier
            if [ "$t" == "ou" ]; then
                elos=("${elos_ou[@]}")
            else
                elos=("${elos_all[@]}")
            fi

            for e in "${elos[@]}"; do

                url=$(printf "%s%s-%s/chaos/gen9%s-%s.json" \
                    "$SMOGUN_URL" \
                    "$y" \
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
done
