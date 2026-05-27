Enable-WindowsOptionalFeature -Online -FeatureName `
"IIS-WebServerRole", `
"IIS-WebServer", `
"IIS-CommonHttpFeatures", `
"IIS-ApplicationDevelopment", `
"IIS-ASPNET45", `
"IIS-NetFxExtensibility45", `
"IIS-ISAPIFilter", `
"IIS-ISAPIExtensions" `
 -All -NoRestart
