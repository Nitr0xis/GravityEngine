# Security Policy

GravityEngine is a local desktop physics simulation. It doesn't handle credentials, doesn't access the network, and doesn't process sensitive data. Security surface is small, but reasonable precautions still apply.

## Scope

**What the application does:**

- Renders graphics via Pygame, reads mouse/keyboard input
- Runs physics calculations locally
- Reads `assets/` (fonts, icons) and writes to `user_data/` (config, logs, screenshots) — or `Documents/GravityEngine/` in exe builds
- Runs entirely with user-level permissions

**What it never does:**

- Access the network
- Write to system directories or the registry
- Access personal files outside its own `user_data/` folder
- Use webcam/microphone
- Require admin/root
- Execute shell commands or use `eval()`/`exec()`

If the executable ever asks for admin rights, firewall access, or write access outside its own data folder — that's a red flag. Report it.

## Reporting a Vulnerability

Do not open a public issue for security reports. Email [nils.dontot.pro@gmail.com](mailto:nils.dontot.pro@gmail.com) with subject `[SECURITY] Brief description`, including steps to reproduce, impact, and environment (OS, Python version).

Expect acknowledgment within 48 hours and an initial assessment within 7 days. Fix timeline depends on severity — critical issues are prioritized, cosmetic ones may wait for the next release. Coordinated disclosure preferred; researchers are credited unless they request anonymity.

## Known Considerations

- **Executables:** only download from [official releases](https://github.com/Nitr0xis/GravityEngine/releases). Third-party mirrors aren't trusted.
- **Dependencies:** Pygame and matplotlib, both actively maintained. No pinned-version guarantees yet — check `pip list --outdated` if concerned.
- **Path handling:** asset loading resolves paths via `Atlas.resource_path()`; report any path that escapes the `assets/`/`user_data/` folders.

## For Contributors

- Validate inputs at function boundaries (types, ranges) rather than assuming well-formed calls.
- Never construct file paths by direct string interpolation of external input; resolve and check the path stays within the intended base directory.
- Pin dependency versions in build/release configs where practical.

## License

Copyright (c) 2026 Nils DONTOT

Copyleft license: you may use, study, modify, and redistribute this software freely, including commercially. Any distributed modified version must remain licensed under GPL-3.0 and its source code must be made available to recipients.

Preservation of reasonable legal notices or author attributions, as permitted by Section 7(b), is required: if you modify this Program, or any covered work, and distribute a modified version, you must preserve reasonable attribution to the original author (Nils DONTOT) in any "About", credits screen, or README file of the resulting work.

See [LICENSE](LICENSE) — full terms at [gnu.org/licenses/gpl-3.0](https://www.gnu.org/licenses/gpl-3.0).

*Last updated: August 2026 — v3.9.0*
