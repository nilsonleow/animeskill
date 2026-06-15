# xAI Grok Imagine Notes

Use `grok-imagine-video` through xAI's video generation endpoint for image-to-video.

## Endpoint

- Start generation: `POST https://api.x.ai/v1/videos/generations`
- Poll generation: `GET https://api.x.ai/v1/videos/{request_id}`
- Auth: `Authorization: Bearer $XAI_API_KEY`

## Request Shape

```json
{
  "model": "grok-imagine-video",
  "prompt": "Animate the character...",
  "image": { "url": "data:image/png;base64,..." },
  "duration": 2,
  "aspect_ratio": "1:1",
  "resolution": "720p"
}
```

The image may be a public URL, base64 data URI, or xAI Files API `file_id`. For local agent workflows, base64 data URI is simplest.

## Supported Project Defaults

- Duration: only `1`, `2`, or `3` seconds for this skill.
- Size: `480x480` maps to `resolution: "480p"` and `aspect_ratio: "1:1"`.
- Size: `720x720` maps to `resolution: "720p"` and `aspect_ratio: "1:1"`.
- Output video URL is temporary. Download it immediately.

## Pricing Defaults

As of the June 2026 xAI pricing page:

- `grok-imagine-video` 480p output: `$0.05/sec`.
- `grok-imagine-video` 720p output: `$0.07/sec`.
- Image input: `$0.002/img`.

Always present estimated cost before generation and get confirmation.

## Failure Handling

- `pending`: wait and poll again.
- `done`: download `video.url`.
- `failed` or `expired`: report the status and response body.
- API errors may still be billable depending on moderation and generation status.
