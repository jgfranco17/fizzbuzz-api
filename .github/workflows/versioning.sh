#!/bin/bash

# Assuming the JSON file is in a neighboring directory named 'data'
file_path="../../specs.json"

# Read JSON data from the file
data=$(cat "$file_path")

# Extract version and lastUpdatedOn values
version=$(cat "api/VERSION")
lastUpdatedOn=$(jq -r '.lastUpdatedOn' <<< "$data")

# Increment version
IFS='.' read -r major minor patch <<< "$version"
patch=$((patch + 1))
new_version="${major}.${minor}.${patch}"

# Update lastUpdatedOn
new_lastUpdatedOn=$(date -u +"%Y-%m-%dT%H:%M:%S.%NZ")

# Update JSON data
updated_data=$(jq --argjson version "$new_version" --arg lastUpdatedOn "$new_lastUpdatedOn" \
    '.version = $version | .lastUpdatedOn = $lastUpdatedOn' <<< "$data")

# Write updated data back to the file
echo "$updated_data" > "$file_path"
