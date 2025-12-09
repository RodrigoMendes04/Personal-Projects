# 🤖 Automated Job Hunter Pipeline

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![SQLite](https://img.shields.io/badge/SQLite-Database-lightgrey)
![Discord](https://img.shields.io/badge/Discord-Webhooks-7289DA)
![Status](https://img.shields.io/badge/Status-Active-success)

> **Stop scrolling, start automating.** A smart data pipeline that scrapes, filters, and delivers relevant job opportunities directly to Discord in real-time.

## 📖 Overview

Searching for a job manually is inefficient. This project automates the process by monitoring multiple high-quality job boards (WeWorkRemotely, RemoteOK) via RSS feeds. It applies intelligent text filtering to separate "Junior/Mid-level" roles from "Senior/Manager" roles and delivers a rich notification card to a Discord channel.

It features a built-in **SQL deduplication layer**, ensuring you never receive the same job alert twice.

## 🏗️ Architecture

The system follows a modular "Extraction-Transformation-Load" (ETL) pattern:

```mermaid
graph LR
    A[RSS Feeds] -->|Extract| B(Scraper Module)
    B -->|Transform| C{Filter Logic}
    C -- "Senior/Manager" --> D[Discard]
    C -- "Relevant Tech" --> E{Check DB}
    E -- "Duplicate" --> D
    E -- "New Job" --> F[(SQLite DB)]
    F -->|Load/Notify| G[Discord Webhook]
