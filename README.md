# Lighthouse client
![](https://github.com/RobinSiep/lighthouse-client/workflows/Test%20%26%20Deploy/badge.svg)

Client-side application for [Lighthouse](https://github.com/RobinSiep/lighthouse-client), a tool to manage machines over a variety of networks.

## Requirements
You will need an OAuth client id and client secret from Lighthouse.

### Wake-on-LAN
Lighthouse supports Wake-on-LAN to power on a machine through another machine. In order for a machine to be able to **send** the packet [wakeonlan](https://launchpad.net/ubuntu/+source/wakeonlan) needs to be installed. In order for a machine to be able to **receive** the packet and function accordingly Wake-on-LAN needs to be turned on in the BIOS and in the operating system of choice.

## Installation & Usage

## From source
```
pip install -e .
lighthouseclient <YOUR LIGHTHOUSE HOST> '<YOUR CLIENT ID>' '<YOUR CLIENT SECRET>'
```

## Using Docker
I don't recommend using Docker for this package at this point. Instead of using the host system metrics it will send those of the container to Lighthouse which isn't incredibly useful.

If you do decide to use Docker keep in mind you need to run the container with network mode `host` which is currently only supported on Linux. Otherwise it'll publish the network interfaces on the container which means that things like Wake-on-LAN will **not** work.

```
docker run -d mellow/lighthouse-client:latest <YOUR LIGHTHOUSE HOST> '<YOUR CLIENT ID>' '<YOUR CLIENT SECRET>'
```

## Note
This project is still very much a work in progress. Its documentation and test coverage are not up to standards.
