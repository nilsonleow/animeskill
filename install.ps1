param(
    [string]$RepoZipUrl = "https://github.com/nilsonleow/animeskill/archive/refs/heads/main.zip",
    [string]$Destination = "$env:USERPROFILE\.codex\skills\animeskill",
    [switch]$ConfigureKey
)

$ErrorActionPreference = "Stop"

function Write-Step($Message) {
    Write-Host "[animeskill] $Message"
}

$tempRoot = Join-Path ([System.IO.Path]::GetTempPath()) ("animeskill-install-" + [System.Guid]::NewGuid().ToString("N"))
$zipPath = Join-Path $tempRoot "animeskill.zip"
$extractPath = Join-Path $tempRoot "extract"

try {
    New-Item -ItemType Directory -Force $tempRoot | Out-Null

    Write-Step "Downloading $RepoZipUrl"
    Invoke-WebRequest -Uri $RepoZipUrl -OutFile $zipPath

    Write-Step "Extracting archive"
    Expand-Archive -Path $zipPath -DestinationPath $extractPath

    $source = Get-ChildItem -Path $extractPath -Directory |
        Select-Object -First 1 |
        ForEach-Object { Join-Path $_.FullName "skills\animeskill" }

    if (-not (Test-Path (Join-Path $source "SKILL.md"))) {
        throw "Could not find skills/animeskill/SKILL.md in downloaded archive."
    }

    Write-Step "Installing to $Destination"
    if (Test-Path $Destination) {
        Remove-Item -Recurse -Force $Destination
    }
    New-Item -ItemType Directory -Force (Split-Path $Destination) | Out-Null
    Copy-Item -Recurse $source $Destination

    $cachePath = Join-Path $Destination "scripts\__pycache__"
    if (Test-Path $cachePath) {
        Remove-Item -Recurse -Force $cachePath
    }

    $required = @(
        "SKILL.md",
        "agents\openai.yaml",
        "references\prompting.md",
        "references\xai-imagine.md",
        "scripts\configure_xai_key.py",
        "scripts\generate_xai_video.py"
    )

    foreach ($relativePath in $required) {
        $fullPath = Join-Path $Destination $relativePath
        if (-not (Test-Path $fullPath)) {
            throw "Installed skill is missing $relativePath"
        }
    }

    Write-Step "Installed successfully."
    Write-Host ""
    Write-Host "Restart Codex to pick up the installed skill."
    Write-Host ""
    Write-Host "Configure xAI API key:"
    Write-Host "python `"$Destination\scripts\configure_xai_key.py`""
    Write-Host ""
    Write-Host "Then use:"
    Write-Host 'Use $animeskill to animate @path/to/character.png into a 1-second crouch animation at 480x480 on #00FF00.'

    if ($ConfigureKey) {
        Write-Host ""
        Write-Step "Starting key configuration"
        python "$Destination\scripts\configure_xai_key.py"
    }
}
finally {
    if (Test-Path $tempRoot) {
        Remove-Item -Recurse -Force $tempRoot
    }
}
