# Serial Frame Analyzer

A high-performance Python utility designed to parse, validate, and decode binary serial protocols. This tool mimics the functionality of a protocol sniffer for embedded systems, specifically targeting frame structures similar to the Silicon Labs BGAPI.

## Overview

The **Serial Frame Analyzer** serves as a bridge for developers to interpret raw binary streams from wireless SoCs. It automates the extraction of message types, class IDs, and payloads while ensuring data integrity via checksum validation.

## Key Features

- **Binary Parsing:** Decodes structured headers (Type, Length, Class ID, Message ID).
- **Data Integrity:** Implements CRC-16/CCITT-FALSE validation to ensure frame reliability.
- **Protocol Mapping**: Translates raw hex IDs into human-readable Enums (e.g., SYSTEM, DFU).
- **Observability**: Integrated Python logging for professional error tracking and debugging.
- **CI/CD Integrated:** Automated testing suite triggered via GitHub Actions.

## Project Structure (SDLC Evidence)

This repository follows a full Software Development Life Cycle approach:
- `/docs`: Contains `requirements.md` (Analysis) and `architecture.md` (Design).
- `/src`: Modular source code (Implementation).
- `/tests`: Automated unit tests using `pytest` (Verification).
- `.github/workflows`: Continuous Integration pipeline (Maintenance).

## Quick Start

### Installation
```bash
git clone [https://github.com/P-Andras/serial-frame-analyzer.git](https://github.com/P-Andras/serial-frame-analyzer.git)
cd serial-frame-analyzer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Usage
```bash
python3 -m src.main "00020105AABBD233"
```

### Running Tests
```bash
python3 -m pytest tests/
```