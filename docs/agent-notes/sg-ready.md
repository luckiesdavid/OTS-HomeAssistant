# SG Ready room setpoint increase

The catalog contains one APK-labelled point per heating circuit named
"Heizkreis X - Raumsollwert - Erhöhung Heizen" ("Room target value - Increase
heating"). This is the room setpoint increase applied in the SG Ready state.
The accountless catalog shipped it as a read-only `sensor`, because the
reference plant supplied no write binding for it.

| Circuit | Read and write OA | Range (K) | Step (K) |
| --- | --- | --- | --- |
| 1 | `ACONg458AAE=` | 0–5 | 0.5 |
| 2 | `ACONg+1MAAE=` | 0–5 | 0.5 |
| 3 | `ACONg8xcAAE=` | 0–5 | 0.5 |
| 4 | `ACONgyssAAE=` | 0–5 | 0.5 |

## Evidence and limits

- Object type 0, member 1. That matches parameters the reference plant
  confirms are written to their read address, such as "Heizkurve
  Bezugsraumtemperatur" (`ACNx1I58AAE=`). Measured values such as
  `CiPcW458AAE=` use a different object type.
- The range and step were reported by a user. They are not transcribed from
  the APK. The Smart app APK could not be downloaded from the build
  environment. Bindings are therefore marked `write_source: user_reported`.
- No controller write has been tested. If the controller rejects a write,
  the integration reports the error and no value changes.

To confirm, compare the app's range for this setting. Then write a value
once with `tools/climatix_local_api.py` and read it back. After a confirmed
APK transcription, move the bindings to `APK_NUMBER_BINDINGS`.

Existing users can select **Local catalog scan now (accountless; add missing
entities)** in the integration options after updating. This adds the
`number` entities and keeps the old sensors.
