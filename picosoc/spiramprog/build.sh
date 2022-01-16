#!/usr/bin/env bash

rm -rf build
mkdir build
yosys -p 'synth_ice40 -top passthrough -json build/project.json' ./mch2022v2_passthrough.v
nextpnr-ice40 --up5k --package sg48 --json build/project.json --pcf mch2022v2.pcf --asc build/proto2.asc
icepack build/proto2.asc build/proto2.bin