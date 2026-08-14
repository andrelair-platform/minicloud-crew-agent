# Changelog

## [1.1.0](https://github.com/andrelair-platform/minicloud-crew-agent/compare/minicloud-crew-agent-v1.0.1...minicloud-crew-agent-v1.1.0) (2026-08-14)


### Features

* **ci:** add dev branch build — tags dev-&lt;sha&gt;, updates dev gitops overlay ([f363519](https://github.com/andrelair-platform/minicloud-crew-agent/commit/f3635190f3c21ce6d8f27ba9fff0ab3534e8c0a2))
* initial service extraction from minicloud-gitops ([7beb2d7](https://github.com/andrelair-platform/minicloud-crew-agent/commit/7beb2d72dd7876759345bbbe60880bee68542cac))


### Bug Fixes

* **ci:** direct PR merge (auto-merge disabled on minicloud-gitops) ([f44c4c9](https://github.com/andrelair-platform/minicloud-crew-agent/commit/f44c4c9618868aa9646372352f2c906827051cc6))
* **ci:** GPG-sign gitops commit and use PR flow (main branch is protected) ([1ff6d95](https://github.com/andrelair-platform/minicloud-crew-agent/commit/1ff6d95dba73374172d652647deda0b2cf2f2b7a))
* **ci:** restart Docker daemon after CA cert injection for buildx ([263e007](https://github.com/andrelair-platform/minicloud-crew-agent/commit/263e007b879aa3b3dde5e16ede63bf31f0b0e035))
* **ci:** use buildkitd insecure=true for Harbor (buildx container can't see host CA) ([6247bb5](https://github.com/andrelair-platform/minicloud-crew-agent/commit/6247bb53373ddae1e0c111f634369aa5e729ea5b))
* **lint:** sort imports, fix line length, drop isort rule ([2b5bb4d](https://github.com/andrelair-platform/minicloud-crew-agent/commit/2b5bb4d739cf1a6b274eca076e3ac35379fee658))
* **tests:** real BaseTool stub, correct patch target, exclude AI files from coverage ([4a13790](https://github.com/andrelair-platform/minicloud-crew-agent/commit/4a13790b3152c74b93350a24bdd535c449d3f1ef))

## Changelog

All notable changes to minicloud-crew-agent are documented here.

This file is maintained by [release-please](https://github.com/googleapis/release-please).
