# Hardcoded ASP.NET Machine Key Vulnerability & Exploitation Demo

This is a repository dedicated for educational testing of IIS Web Server exploitation via a simulation of a standardized web.config file provided typically by a vendor in many cases. This configuration file contains hardcoded machineKey values used by the ASP.NET framework to encrypt and sign data, including ViewState payloads. This allows an attacker to construct a malicious ViewState payload and potentially execute code in the context of the IIS worker process (w3wp.exe).

Although the issue of hardcoded machine keys and associated exploitation has been known for years, it continues to crop up year after year, including in the following recent major campaigns:

**USAHERDS RCE** - CVE-2021-44207
**CentreStack RCE** - CVE-2025-30406
**Sitecore RCE** - CVE-2025-53690
**KnowledgeDeliver RCE** - CVE-2026-5426


# Setting up the vulnerable IIS Server
First, you will need a Windows Server variant with the IIS server role enabled. 

After the IIS Server role is enabled, run the **Enable-IISFeatures.ps1** script with administrative privileges to enable ASP.NET features.

Then, place **web.config** and **vuln.aspx** in **C:\inetpub\wwwroot**, then run the command **iisreset** from an administrative Powershell session.

At this point, you should then be able to browse to http://Local_Server_IP_here/vuln.aspx and see the basic web application in use to verify IIS/ASP.NET is set up properly.

# Testing the Exploit Locally
