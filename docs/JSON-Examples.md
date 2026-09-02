# Wayfinder JSON Examples

```json
{
  "status": "ok",
  "tool": "wayfinder",
  "version": "0.1.0",
  "data": {
    "entity": {
      "id": "zoning",
      "title": "Zoning",
      "physical_path": "D:\\.zoning",
      "manifest_path": "D:\\.zoning\\.zoning.manifest.toml"
    }
  }
}
```

```json
{
  "status": "error",
  "tool": "wayfinder",
  "version": "0.1.0",
  "data": {},
  "errors": [{"code": "not-found", "message": "No entity matches: unknown", "severity": "error"}]
}
```
