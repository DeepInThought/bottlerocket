{ stdenvNoCC, lib, config, rpm, rpm-macros, rpm-dependencies, mkMacroPath, tharPackages, ... }:
let
  # TODO: use cross arch here

  # Architecture specific macros
  arch-macros = "${rpm-macros.arches}/x86_64";
  # The base set of thar macros
  thar-macros = map (n: "${rpm-macros.out}/${n}") [ "shared" "rust" "cargo" ];
  # RPM distributed macros
  rpm-dist-macros = "${rpm}/lib/rpm/macros";
  # Macro path for rpm tools
  macroPath = lib.concatStringsSep ":" (lib.flatten [ arch-macros thar-macros rpm-dist-macros ]);
in
{ name, spec, sources, ... }:
let
  # passthru data for the derivation - this *does* require the
  # derivation to build, which is somewhat uncharacteristic of
  # typical passthru usage.
  passthru = with lib; let
    fileList = file: remove "" (splitString "\n" (fileContents "${drv}/${file}"));
    # List of BuildRequires (all, including thar) stated from parsed spec.
    buildRequires =  fileList "buildRequires";
    # List of BuildRequires depending on host system stated from parsed spec.
    hostBuildRequires = fileList "hostBuildRequires";
    # List of provided capabilities.
    provides = fileList "provides";
    # List of packages required at runtime.
    requires = fileList "requires";
    # List of sources that are referenced in parsed spec along with
    # their hashes.
    sources = with builtins; (fromJSON (fileContents "${drv}/sources.json")).sources;
    # Handle processing of rpm metadata to find dependencies as needed.
    dependentPackages = rpm-dependencies { requires = buildRequires; };
  in {
    inherit spec sources
      buildRequires hostBuildRequires
      requires provides
      macroPath dependentPackages;
    macros = thar-macros ++ [ arch-macros ];
  };

  drv = stdenvNoCC.mkDerivation {
    inherit passthru;

    name = "${name}-metadata";

    phases = [ "parsePhase" "generatePhase" ];

    buildInputs = [ rpm ];

    # Parse the rpm spec to extract metadata.
    parsePhase = ''
    echo "$macroPath"
    mkdir -p $out

    # Write out fully rendered spec file
    rpmspec "--macros=${macroPath}" --define "_sourcedir ./" --parse "${spec}" > $out/parsed.spec

    # Write out BuildRequires Requires and Provides
    rpmspec "--macros=${macroPath}" --define "_sourcedir ./" --query --buildrequires "${spec}" > $out/buildRequires
    grep --word-regexp "thar" --invert-match $out/buildRequires > $out/hostBuildRequires || : ignore no matches
    rpmspec "--macros=${macroPath}" --define "_sourcedir ./" --query --requires "${spec}" > $out/requires
    rpmspec "--macros=${macroPath}" --define "_sourcedir ./" --query --provides "${spec}" > $out/provides

    if grep -o -E '^Source[0-9]+:.*http.*$' "$out/parsed.spec" \
       | sed 's/Source.*:.*http/http/' \
       | grep -v -e '^$' -e '.crate$' \
       | tee remote-source-urls; then
      echo "Collecting sources for package"
    else
      echo "Package has no sources"
    fi
    '';

    generatePhase = ''
    declare -A source_hash_entry

    # Ugh, sort the damn thing.
    tac remote-source-urls | sort | tee remote-sources-urls

    while read source_url; do
      echo "Generating source entry for $source_url"
      FILENAME="''${source_url##*/}"
      # ALGO-HASH_CONTENT - https://www.w3.org/TR/SRI/
      SRI="$(awk -v filename="($FILENAME)" '$2 == filename {print tolower($1)"-"$4}' ${sources})"
      test -n "$SRI" || exit 1
      source_hash_entry["$source_url"]="$SRI"
    done < remote-source-urls

    json_entries=""
    for url in "''${!source_hash_entry[@]}"; do
      if [[ -n "$json_entries" ]]; then json_entries="$json_entries, "; fi
      urlHash="''${source_hash_entry[$url]}"
      # SRI prefixed with algo
      urlHashAlgo="''${urlHash%%-*}"
      # Stripped hash
      urlAlgoHash="''${urlHash##*-}"
      entry="$(printf '{"url": "%s", "%s": "%s"}' "$url" "$urlHashAlgo" "$urlAlgoHash")"
      json_entries+="$entry"
    done
    printf '{"sources": [%s]}' "$json_entries" > "$out/sources.json"
    '';
  };
in
drv
