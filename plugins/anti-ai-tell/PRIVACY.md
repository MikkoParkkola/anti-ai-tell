# Privacy

anti-ai-tell runs on your machine. It reads the files and text you ask it to lint, and an optional local style fingerprint when you have created one.

The lint command reads the path you name. The lint-on-write hook does the same for the file just saved, and it also reads `fingerprint.json` from the working directory when that file exists. The session hook reads the fingerprint too, so the agent can see the accent and font you set. A design prompt can trigger a local look at unset slots. Drafts stay put.

What it stores is narrower. Only the local fingerprint files you create, such as `fingerprint.json` in the project, are written for this purpose. The plugin does not open an account. It does not keep a log of your drafts, and it does not write a second copy of your text. It also stores a random install id under `~/.anti-ai-tell/telemetry`, and a machine id shared with the other products under `~/.revaluator/machine-id`.

What it sends is nothing about those drafts. User text is not sent to the author. The lint result, the file path, and the fingerprint are not sent to the author.

The session hook and the lint command send at most one POST per day to `https://telemetry.revaluator.ai/v1/heartbeat`. They share one install id and one daily stamp, so a day produces one attempt. The JSON fields are `project` (`anti-ai-tell`), `event` (`heartbeat`), `version`, `runtime` (operating system, architecture, and the Python version), `install_id`, `install_date`, and `machine_id`. The install id is 16 random bytes, stored on this machine, and created once for this product. `install_date` is the UTC date that id was created. Later heartbeats send that same date, so the cohort is still known after older rows age out. `machine_id` is another 16 random bytes, stored in `~/.revaluator/machine-id` and shared by the products on this machine, so those products can be matched to the same machine. It is not a name, an email, or an account. The request times out after 3 seconds, and a failed send is ignored.

Cloudflare terminates that connection, so Cloudflare can see the caller IP. The receiver stores the connection's city name and country code. Coordinates and the IP are not written into the stored point. Records stay in Cloudflare Analytics Engine for three months.

Development builds, tests, and CI skip this POST. Set `ANTI_AI_TELL_NO_TELEMETRY`, `NO_TELEMETRY`, or `DO_NOT_TRACK` to a value other than `0` or `false` to turn it off. `ANTI_AI_TELL_TELEMETRY_ENDPOINT` replaces the URL. An empty value leaves the default.

Support is Mikko Parkkola via GitHub issues at https://github.com/MikkoParkkola/anti-ai-tell/issues.
