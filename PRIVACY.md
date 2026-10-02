# Rankbeam for Laravel: data handling

Effective 2 October 2026. Publisher: Valentin Goxhaj, Rankbeam. Contact: hello@rankbeam.dev.

This notice describes the Rankbeam for Laravel agent plugin. The plugin contains instructions and local PHP helper scripts. It has no Rankbeam backend, analytics endpoint, account system, cookies or automatic telemetry.

## Local project and HTML data

The project inspector reads selected dependency names and version constraints from `composer.json` and `composer.lock`, checks for application files and lists candidate source paths. It does not read environment files, credentials or application database records, and does not execute the application's PHP code.

The HTML checker reads the local `.html` or `.htm` file supplied to it and outputs counts, findings and limitations. It does not retrieve remote pages, execute scripts or send the file to Rankbeam.

The agent may read relevant application source, run authorized Laravel commands, query the application's configured database or make requested edits as part of the task. Those actions occur through the host application's tools and permissions. You should use a local or test environment and provide only the project/data needed for the task.

## Recipients and retention

The bundled helpers send no project content, HTML, findings or personal data to the publisher. They do not persist the input or results themselves. Console output, saved reports, conversation history and other files may be retained by your agent host or your own tooling. Their processing, recipients and retention are governed by that host's settings and policies. Delete local outputs and manage conversation history through those tools.

Opening documentation or running Composer can contact the documentation host, package registries and package-source hosts. Your application can also have its own network activity when Artisan boots its service providers. Those services apply their own data policies; the plugin does not introduce a separate data relay.

## Support you choose to request

Do not send secrets, production data or unredacted customer content in support requests. Public GitHub issues and their history are hosted by GitHub and are visible to others. If you email the support address, the publisher receives the address and content you choose to send through the existing email provider. This correspondence is used to respond to and track your request, is retained while needed to resolve and follow up on it, and can be reviewed or deleted on request unless retention is otherwise required. It is not needed to use the plugin.

Uninstalling the plugin removes its availability in your agent host. It does not revert application changes, uninstall Composer packages or delete reports created during your tasks.
