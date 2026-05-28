# Hardcoded ASP.NET Machine Key Vulnerability & Exploitation Demo

This is a repository dedicated for educational testing of IIS Web Server exploitation via a simulation of a standardized web.config file provided typically by a vendor in many cases. This configuration file contains hardcoded machineKey values used by the ASP.NET framework to encrypt and sign data, including ViewState payloads. This allows an attacker to construct a malicious ViewState payload and potentially execute code in the context of the IIS worker process (w3wp.exe).

Although the issue of hardcoded machine keys and associated exploitation has been known for years, it continues to crop up year after year, including in the following recent major campaigns:

[**USAHERDS RCE** - CVE-2021-44207](https://cloud.google.com/blog/topics/threat-intelligence/apt41-us-state-governments)

[**CentreStack RCE** - CVE-2025-30406](https://www.huntress.com/blog/cve-2025-30406-critical-gladinet-centrestack-triofox-vulnerability-exploited-in-the-wild)

[**Sitecore RCE** - CVE-2025-53690](https://cloud.google.com/blog/topics/threat-intelligence/viewstate-deserialization-zero-day-vulnerability)

[**KnowledgeDeliver RCE** - CVE-2026-5426](https://cloud.google.com/blog/topics/threat-intelligence/knowledgedeliver-viewstate-deserialization-vulnerability/)



# Setting up the vulnerable IIS Server
First, you will need a Windows Server variant with the IIS server role enabled. 

After the IIS Server role is enabled, run the **Enable-IISFeatures.ps1** script with administrative privileges to enable ASP.NET features.

Then, place **web.config** and **vuln.aspx** in **C:\inetpub\wwwroot**, then run the command **iisreset** from an administrative Powershell session.

At this point, you should then be able to browse to <code>http://Local_Server_IP_here/vuln.aspx</code> and see the basic web application in use to verify IIS/ASP.NET is set up properly.

**Do not expose this server to the internet or untrusted networks**



# Testing the Exploit Locally

The exploit script, **pop_viewstate.py**, is designed to be run from Linux, so Wine with dotnet48 functionality is necessary to work out of the box. Getting wine to execute ysoserial.exe is left as an exercise to the reader. Alternatively, one can run the exploit payload from a Windows device.

The script expects an IP address as the sole command line argument ( <code> target = sys.argv[1] </code> ). This IP address should be the IP of the IIS server configured earlier. The payload command is set to calc.exe for demonstration purposes, and is defined in the ysoserial command.

With the IIS server running and accessible from the exploiting machine, run
<code> ./pop_viewstate.py 192.168.0.5 </code>, replacing the target IP address where applicable. If the exploit is successful, the IIS server returns an HTTP response code of 500, which will be notated in the script output:

<img width="738" height="261" alt="image" src="https://github.com/user-attachments/assets/1355647b-e2e1-4d01-afdc-62e13007ec6d" />

At this point, you should also be able to see a calc.exe (or equivalent) process running under the context of the **iis apppool\defaultapppool** user if running a <code>tasklist | sls calc</code> command in Powershell on the IIS server.

<img width="1724" height="504" alt="hardcoded_machine_key_exploit" src="https://github.com/user-attachments/assets/eaf5535c-84ec-44b3-92d6-36cce8ad41a2" />



# Detecting the Exploitation

As this particular exploit relies on spawning a subprocess from w3wp.exe, the IIS worker process, this generates an Event ID 4688 event in the Windows Event Log that can be viewed. If event ID 4688 is enabled, and command line auditing is also enabled for this event, we can see the DefaultAppPool account spawning a cmd.exe command with arguments to launch calc.exe. The parent process of this activity is w3wp.exe, the IIS worker process.

<img width="656" height="559" alt="image" src="https://github.com/user-attachments/assets/a5c37a08-1618-4380-b747-a51d468fb1e9" />

As such, [it is relatively easy to detect](https://redcanary.com/blog/threat-detection/detecting-sharepoint-attacks-via-worker-process-activity/), as well as create detection rules for some of this activity. Real-world exploitation typically spawns subprocesses in a more subtle manner, or potentially rely on loading and executing an arbitrary .NET assembly directly into the memory of the w3wp.exe process, negative the need to spawn a subprocess. Such in-memory activity could be detected based on unusual file accesses, file writes, or outbound network connections from the w3wp.exe process, which would rely on Sysmon or other EDR-type products that have that level of monitoring functionality. However, for educational purposes, this demonstrates the vulnerability and its implications.



