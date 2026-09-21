# Stage 7 — update.escloud.us Ingress Redirect Correction — 2026-09-21

## Result

**COMPLETE / ACCEPTED**

`STAGE07_UPDATE_ROOT_REDIRECT_FIX=PASS`

## Symptom

Opening the canonical maintenance URL `https://update.escloud.us/` authenticated through the public ingress and then led the browser to:

```text
http://update.escloud.us:18070/status/
```

The destination was unreachable because TCP/18070 is intentionally a loopback-only application backend and is not exposed through UFW.

## Root cause

The public nginx virtual host proxies authenticated requests to the internal dashboard nginx at `127.0.0.1:18070` and preserves the public `Host` header. The internal root location returned a relative target:

```nginx
location = / {
    return 302 /status/;
}
```

nginx uses absolute redirects by default. At this inner proxy layer it therefore serialized the target with its own listener scheme and port, producing `Location: http://update.escloud.us:18070/status/`. The outer reverse proxy passed that header to the client unchanged.

## Recovery checkpoint

Before mutation, the active internal and public nginx virtual-host files, complete `nginx -T` output and SHA-256 manifest were saved at:

```text
/srv/backups/edge-stage7-update-redirect/recovery-20260921T102729Z
```

Pre-change internal virtual-host SHA-256:

```text
cf4890ad5be72de83658c975232e72b03f155ad27459833704c3cdddacadce96
```

The public virtual host was not changed. Its SHA-256 remained:

```text
fc4ea6b4d120d202747a2a651867afa45c370a86cd92506758d15dc6ec6fbb7a
```

## Correction

The internal root location now disables absolute redirect construction locally:

```nginx
location = / {
    absolute_redirect off;
    return 302 /status/;
}
```

The change is intentionally scoped to this location. It preserves the root-to-status navigation while preventing the loopback server's scheme and port from leaking into the public response.

Post-change internal virtual-host SHA-256:

```text
772570336fe25da5e1c210ba2bca5ef3cf20b453ae9c4c0659d543de9191a20f
```

## Verification

- `nginx -t`: PASS before and after installation;
- internal root with the public Host header: HTTP 302 with exactly `Location: /status/`;
- internal `/status/`: HTTP 200, 52,825-byte response;
- public HTTP root: HTTP 301 to `https://update.escloud.us/`;
- public HTTPS root without an authenticated session: HTTP 302 to `https://auth.escloud.us/` with return destination `https://update.escloud.us/`;
- public TCP/18070 connection: rejected/unreachable as intended;
- listener: `127.0.0.1:18070` only;
- UFW: unchanged; no TCP/18070 rule;
- nginx service: active/running, zero restarts caused by the correction;
- nginx error log after reload: empty.

An authenticated browser traversal was not available in the maintenance shell. The corrected boundary was verified directly against the internal server using the public Host header, and the unchanged public authentication boundary was verified independently.

## Mechanism references

- nginx `absolute_redirect`: <https://nginx.org/en/docs/http/ngx_http_core_module.html#absolute_redirect>
- nginx proxy redirect handling: <https://nginx.org/en/docs/http/ngx_http_proxy_module.html#proxy_redirect>

## Accepted contract

- operator entry point: `https://update.escloud.us/`;
- successful authentication returns the operator to the same public origin;
- root navigation resolves to `https://update.escloud.us/status/` in the browser;
- TCP/18070 remains private and must never appear in a public redirect;
- the Stage 7 manual-update policy remains unchanged.
