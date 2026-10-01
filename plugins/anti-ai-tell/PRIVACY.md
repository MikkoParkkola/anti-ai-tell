# Privacy

anti-ai-tell runs on your machine. It reads the files and text you ask it to lint, and an optional local style fingerprint when you have created one.

The lint command reads the path you name. The lint-on-write hook does the same for the file just saved, and it also reads `fingerprint.json` from the working directory when that file exists. The session hook reads the fingerprint too, so the agent can see the accent and font you set. A design prompt can trigger a local look at unset slots. Drafts stay put.

What it stores is narrower. Only the local fingerprint files you create, such as `fingerprint.json` in the project, are written for this purpose. The plugin does not open an account. It does not keep a log of your drafts, and it does not write a second copy of your text.

What it sends is nothing about those drafts. User text is not sent to the author or to a telemetry endpoint. The linters, hooks, and fingerprint tools do not open a network connection.

Support is Mikko Parkkola via GitHub issues at https://github.com/MikkoParkkola/anti-ai-tell/issues.
