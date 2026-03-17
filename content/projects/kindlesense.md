+++
title = "KindleSense"
description = "Solar-powered LoRa sensor network for wildfire early warning"
date = 2026-03-16
template = "post.html"
insert_anchor_links = "right"

[taxonomies]
tags = ["rust", "embedded", "lora", "esp32", "embassy", "climate", "sensors"]

[extra]
lang = "en"
toc = true
copy = true
comment = false
math = false
mermaid = true
+++

A distributed, solar-powered LoRa sensor network measuring fire-weather conditions in real time.
Dual purpose: a path into climate tech roles, and an eventually-deployable tool for land managers.

> **Status:** Early development — firmware scaffolding complete, LoRa bring-up in progress.
> [View source on GitHub](https://github.com/gazedo/KindleSense)

---

## Motivation

Wildfire behaviour is driven by measurable environmental conditions — air temperature, relative
humidity, wind speed and direction, and the moisture content of dead fuels like leaf litter and
duff.  Professional fire weather frameworks (FWI, NFDRS) turn these into actionable indices that
fire agencies use for suppression planning and prescribed burn windows.

The problem: in remote or roadless terrain, continuous sensor coverage is expensive and
infrastructure-limited.  Cellular-connected weather stations cost thousands of dollars per node.
Battery-powered nodes die quickly.  Solar-powered nodes work if the power budget is right.

LoRa (Long Range radio) enables kilometre-scale wireless links at milliwatt power levels, making
it the correct answer for data-scarce terrain without cellular or grid.  A node that wakes every
60–300 seconds, takes readings, transmits a 20-byte packet, and sleeps again can run indefinitely
on a small solar panel and LiPo cell.

---

## Goals

- **Primary:** portfolio artefact demonstrating prototype-to-production embedded Rust on real
  hardware, for climate tech job applications.
- **Secondary:** real-world deployment — nodes feeding a public Grafana dashboard and optionally
  the Synoptic Data / Weather Underground PWS APIs used by fire agencies.
- **Stretch:** interop with the [Meshtastic](https://meshtastic.org) mesh network so nodes can
  relay data through existing community infrastructure.

---

## Architecture

{% mermaid() %}
flowchart LR
    subgraph Node["Sensor Node (kindle-node)"]
        S[SHT40\nTemp/Humidity] --> MCU
        W[Anemometer\nWind] --> MCU
        F[Dowel Probe\nFuel Moisture] --> MCU
        B[MAX17048\nBattery SOC] --> MCU
        MCU[ESP32-C3\nEmbassy async]
        MCU --> LR1[SX1276\nLoRa TX]
    end

    subgraph Mesh["LoRa Mesh"]
        LR1 -->|flood routing\nhop limit 3| LR2[Relay Node\nkindle-debug]
        LR2 -->|rebroadcast| LR3[More relays...]
    end

    subgraph GW["Gateway (kindle-gateway)"]
        LR3 --> RX[LoRa RX\nHeltec V2]
        RX --> RPi[Raspberry Pi]
        RPi --> IDB[(InfluxDB)]
        IDB --> Graf[Grafana\nPublic Dashboard]
    end
{% end %}

---

## Mesh Routing

The network uses **flood routing with hop-limit deduplication** — the same semantics as
Meshtastic.  Any node that receives a packet it hasn't seen before (tracked by a 64-entry
ring cache of packet IDs) and whose `hop_limit > 0` will decrement the limit and rebroadcast.
This gives roughly 4-hop coverage from any origin with the default limit of 3.

The shared `kindle-proto` crate defines the wire format and routing logic, so embedded nodes and
the Raspberry Pi gateway always agree without duplicating code.

### Packet format

Packets are [postcard](https://github.com/jamesmunns/postcard)-encoded — compact, `no_std`
compatible, and deterministic.  A full sensor reading fits in ~22 bytes.

```
MeshEnvelope {
    from:       u32   // node ID — lower 4 bytes of MAC
    to:         u32   // 0xFFFFFFFF = broadcast
    packet_id:  u32   // random, used for dedup
    hop_limit:  u8    // decremented on each relay (default 3)
    hop_start:  u8    // original hop_limit
    payload:    SensorReading {
        node_id, temp_c (×100), humidity_pct,
        wind_speed_ms (×2), wind_dir_deg,
        fuel_moisture, battery_soc, battery_mv, sequence
    }
}
```

---

## Hardware

### Development — Heltec WiFi LoRa 32 V2

The development target is the Heltec V2: ESP32 + SX1276 + OLED on one board, with a USB
serial port, making it ideal for firmware iteration.  One board runs a known-good Arduino
LoRa TX sketch; the Rust firmware is validated against it before both sides are ported to Rust.

### Production Node — M5Stack Stamp-C3U

| Item | Notes |
|---|---|
| M5Stack Stamp-C3U | ESP32-C3 RISC-V, ~5 µA deep sleep |
| SX1276 | Harvested from spare Heltec V2 boards |
| MAX17048 | I2C fuel gauge, accurate SOC without ADC noise |
| TP4056 + Schottky | LiPo charge with load-sharing |
| SHT40 | Temp + humidity, I2C 0x44 |
| 5–6 V solar panel | ~8 USD |
| 18650 cell | |
| 3D-printed enclosure | Weatherproof, printed in-house |

The ESP32-C3's ~5 µA deep sleep (vs ~800 µA on the Heltec V2) is what makes the solar budget
viable long-term.  A custom KiCad PCB integrating these components is planned for Phase 1.

---

## Firmware Stack

- **Runtime:** [Embassy](https://embassy.dev) async executor — three tasks communicating via
  channels (sensor reading, radio TX, power management)
- **HAL:** `esp-hal` 0.22
- **Radio:** `lora-phy` 3 — async SX127x driver via `embedded-hal-async`
- **Serialization:** `postcard` — `no_std`, no dynamic allocation
- **Logging:** `defmt` over RTT → visible in `espflash --monitor`
- **Power:** adaptive sleep strategy keyed on battery SOC
  (Active ≥50% → LightSleep ≥20% → DeepSleep <20%)

---

## Bring-up Sequence

1. **Arduino loopback** ✓ *(in progress)* — confirm RF link, record modem config
2. **Rust RX ↔ Arduino TX** — `kindle-debug` validating `lora-phy` driver config
3. **Full Rust both sides** — Embassy firmware on both Heltec boards
4. **I2C sensors** — SHT40 first, then MAX17048
5. **Anemometer** — GPIO interrupt pulse counting
6. **RPi gateway** — `kindle-gateway` writing to InfluxDB, Grafana dashboard live
7. **Custom PCB** — KiCad schematic + layout, fabricate at JLCPCB

---

## Crate Structure

```
KindleSense/
├── kindle-proto/    # shared packet types + mesh routing (no_std)
├── kindle-debug/    # LoRa RX + relay firmware — Heltec V2
├── kindle-node/     # sensor node firmware — Stamp-C3U  (planned)
└── kindle-gateway/  # RPi gateway + InfluxDB writer       (planned)
```
