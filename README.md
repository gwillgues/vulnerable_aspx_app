# vulnerable_aspx_app

This is a repository dedicated for educational testing of IIS Web Server exploitation via a simulation of a standardized web.config file provided typically by a vendor in many cases. This configuration file contains hardcoded machineKey values used by the ASP.NET framework to encrypt and sign data, including ViewState payloads. This allows an attacker to construct a malicious ViewState payload and potentially execute code in the context of the IIS worker process (w3wp.exe).

