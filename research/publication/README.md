# Verified GitHub publication — 24 October 2026

The V7 release contains the manuscript, supplement, editable code/report archives, and all 115 lossless raw-data parts for V5–V7. GitHub's recorded SHA-256 digest and byte count matched the manifest for every part. See `V7_RAW_PUBLICATION_MANIFEST.json` for the verification timestamp and archive hashes.

## Download the evidence

Download the V7 code/report archive from:
https://github.com/kaushalrog/Satellite-Optical-Fault-Recovery/releases/tag/research-v7-2026-10-23

Keep `download_v7_raw_data.py` and `V7_RAW_DATA_CHUNKS.json` together. Run:

```sh
python3 download_v7_raw_data.py 7
python3 download_v7_raw_data.py 6
```

The downloader checks each part and the complete reconstructed ZIP. Extract at the same root as the code archive. Version 5 or `all` can be selected for the historical evidence. The V4 release includes the earlier raw archive and full project snapshot.

Maintainers can resume an interrupted upload with `finish_raw_publication.py` after placing original parts in `V7_Raw_Release_Parts/` alongside the script. It needs authenticated GitHub CLI access and verifies the server digests before reporting completion. Run it from the original `output/` directory or copy the manifest and parts alongside it.

## Preserved workspace variants

`Local_Workspace_Overlay_2026-10-24.zip` preserves eight local files that differed from, or supplemented, the published project. Its manifest is stored here and on the release. It is a separate historical overlay: applying it would replace some audited publication files with older local variants, including the V4 integrity report. The published audited files remain authoritative. System caches, operating-system metadata and locally supplied reference PDFs are not project deliverables.
