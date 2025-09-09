Write-up
Analyze, choose, and justify the appropriate resource option for deploying the app

I chose the Azure App Service instead of a VM. The main reasons are:

Cost: App Service is cheaper to run than a VM, which would need extra expenses for OS, storage, and maintenance.

Scalability: It provides easy scaling options, while scaling a VM would require more setup and management.

Availability: App Service handles patches, restarts, and updates automatically, making it more reliable than a VM that I’d have to manage myself.

Workflow: It integrates directly with GitHub, so I can deploy updates quickly. With a VM, I would need to set up and maintain the deployment process manually.

Choice: Based on cost, scalability, availability, and workflow, I chose App Service as the best option for deploying my CMS app.

Assess app changes that would change your decision

I would switch to a VM if the app needed:

Custom OS or software not supported by App Service

Heavy background processing or resource-intensive workloads

Advanced networking or integrations with legacy systems

Strict security and compliance requirements needing custom setups

Otherwise, for my current project, Azure App Service is the most efficient choice.
