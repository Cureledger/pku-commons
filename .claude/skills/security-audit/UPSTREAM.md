# Where this skill comes from

Cloudflare's security-audit skill, copied from
https://github.com/cloudflare/security-audit-skill (`skills/security-audit/`)
at commit c1c8a8c of 14 September 2026. MIT licence: see LICENSE in this folder.

Unchanged, except that the two `*.test.cjs` files, which test the validators,
are left out: a root `vitest run` would pick them up as this repo's tests.

## Using it

Claude Code finds it on its own. Asked a security question or for a focused
review, it uses the parts that apply and writes nothing. Asked to audit the
repo ("security audit this codebase", "quick security audit of worker/"), it
runs the full six-phase workflow: many sub-agents, so a large run. Profiles are
`quick`, `standard` (the default) and `deep`.

A full audit writes its run folder outside the repo, under
`~/security-audit-skill/<repo>/run-<N>`, so findings never land in git unless
someone copies them in. It reads source only; it runs the repo's code only
inside an OS sandbox, and never probes deployed services.

## Updating it

Copy `skills/security-audit/` from upstream again, without the `*.test.cjs`
files, run those tests in the upstream checkout (`node --test`), and change the
commit above.
