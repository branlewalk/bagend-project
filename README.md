# bagend-project

## Overview
This repo is for a homebrew stand device that will read temperatures and then either publish them to a RabbitMq queue, send to a DB or sends directly to a Web App.

The goal is to expand this project from just reporting temps to haveing the device control more aspects of the brew process.

### Hardware Requirements
  - RaspberryPi
  - Breadboard
  - 3 Temperature probes (DS18B20)
  - 1 Perma-Proto Half-sized Breadboard

### Installation

1. Download the repo
   ```sh
   git clone https://github.com/branlewalk/bagend-project.git
   ```
2. Build and Run Docker Image
   ```sh
   bash build-images.sh