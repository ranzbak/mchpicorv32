
CROSS=riscv32-unknown-elf-
CFLAGS=

# ---- iCE40 HX8K Breakout Board ----

hx8ksim: hx8kdemo_tb.vvp hx8kdemo_fw.hex
	vvp -N $< +firmware=hx8kdemo_fw.hex

hx8ksynsim: hx8kdemo_syn_tb.vvp hx8kdemo_fw.hex
	vvp -N $< +firmware=hx8kdemo_fw.hex

hx8kdemo.blif: hx8kdemo.v spimemio.v simpleuart.v picosoc.v ../picorv32.v
	yosys -ql hx8kdemo.log -p 'synth_ice40 -top hx8kdemo -blif hx8kdemo.blif' $^

hx8kdemo_tb.vvp: hx8kdemo_tb.v hx8kdemo.v spimemio.v simpleuart.v picosoc.v ../picorv32.v spiflash.v
	iverilog -s testbench -o $@ $^ `yosys-config --datdir/ice40/cells_sim.v`

hx8kdemo_syn_tb.vvp: hx8kdemo_tb.v hx8kdemo_syn.v spiflash.v
	iverilog -s testbench -o $@ $^ `yosys-config --datdir/ice40/cells_sim.v`

hx8kdemo_syn.v: hx8kdemo.blif
	yosys -p 'read_blif -wideports hx8kdemo.blif; write_verilog hx8kdemo_syn.v'

hx8kdemo.asc: hx8kdemo.pcf hx8kdemo.blif
	arachne-pnr -d 8k -o hx8kdemo.asc -p hx8kdemo.pcf hx8kdemo.blif

hx8kdemo.bin: hx8kdemo.asc
	icetime -d hx8k -c 12 -mtr hx8kdemo.rpt hx8kdemo.asc
	icepack hx8kdemo.asc hx8kdemo.bin

hx8kprog: hx8kdemo.bin hx8kdemo_fw.bin
	iceprog hx8kdemo.bin
	iceprog -o 1M hx8kdemo_fw.bin

hx8kprog_fw: hx8kdemo_fw.bin
	iceprog -o 1M hx8kdemo_fw.bin

hx8kdemo_sections.lds: sections.lds
	$(CROSS)cpp -P -DHX8KDEMO -o $@ $^

hx8kdemo_fw.elf: hx8kdemo_sections.lds start.s firmware.c
	$(CROSS)gcc $(CFLAGS) -DHX8KDEMO -march=rv32imc -Wl,-Bstatic,-T,hx8kdemo_sections.lds,--strip-debug -ffreestanding -nostdlib -o hx8kdemo_fw.elf start.s firmware.c

hx8kdemo_fw.hex: hx8kdemo_fw.elf
	$(CROSS)objcopy -O verilog hx8kdemo_fw.elf hx8kdemo_fw.hex

hx8kdemo_fw.bin: hx8kdemo_fw.elf
	$(CROSS)objcopy -O binary hx8kdemo_fw.elf hx8kdemo_fw.bin

# ---- iCE40 IceBreaker Board ----

icebsim: icebreaker_tb.vvp icebreaker_fw.hex
	vvp -N $< +firmware=icebreaker_fw.hex

icebsynsim: icebreaker_syn_tb.vvp icebreaker_fw.hex
	vvp -N $< +firmware=icebreaker_fw.hex

icebreaker.json: icebreaker.v ice40up5k_spram.v spimemio.v simpleuart.v picosoc.v ../picorv32.v
	yosys -ql icebreaker.log -p 'synth_ice40 -top icebreaker -json icebreaker.json' $^

icebreaker_tb.vvp: icebreaker_tb.v icebreaker.v ice40up5k_spram.v spimemio.v simpleuart.v picosoc.v ../picorv32.v spiflash.v
	iverilog -s testbench -o $@ $^ `yosys-config --datdir/ice40/cells_sim.v`

icebreaker_syn_tb.vvp: icebreaker_tb.v icebreaker_syn.v spiflash.v
	iverilog -s testbench -o $@ $^ `yosys-config --datdir/ice40/cells_sim.v`

icebreaker_syn.v: icebreaker.json
	yosys -p 'read_json icebreaker.json; write_verilog icebreaker_syn.v'

icebreaker.asc: icebreaker.pcf icebreaker.json
	nextpnr-ice40 --freq 13 --up5k --asc icebreaker.asc --pcf icebreaker.pcf --json icebreaker.json

icebreaker.bin: icebreaker.asc
	icetime -d up5k -c 12 -mtr icebreaker.rpt icebreaker.asc
	icepack icebreaker.asc icebreaker.bin

icebprog: icebreaker.bin icebreaker_fw.bin
	iceprog icebreaker.bin
	iceprog -o 1M icebreaker_fw.bin

icebprog_fw: icebreaker_fw.bin
	iceprog -o 1M icebreaker_fw.bin

icebreaker_sections.lds: sections.lds
	$(CROSS)cpp -P -DICEBREAKER -o $@ $^

icebreaker_fw.elf: icebreaker_sections.lds start.s firmware.c
	$(CROSS)gcc $(CFLAGS) -DICEBREAKER -march=rv32ic -Wl,-Bstatic,-T,icebreaker_sections.lds,--strip-debug -ffreestanding -nostdlib -o icebreaker_fw.elf start.s firmware.c

icebreaker_fw.hex: icebreaker_fw.elf
	$(CROSS)objcopy -O verilog icebreaker_fw.elf icebreaker_fw.hex

icebreaker_fw.bin: icebreaker_fw.elf
	$(CROSS)objcopy -O binary icebreaker_fw.elf icebreaker_fw.bin

# ---- Testbench for SPI Flash Model ----

spiflash_tb: spiflash_tb.vvp firmware.hex
	vvp -N $<

spiflash_tb.vvp: spiflash.v spiflash_tb.v
	iverilog -s testbench -o $@ $^

# ---- iCE40 Upduino V3 Board ----

upd3sim: upd3reaker_tb.vvp upd3reaker_fw.hex
	vvp -N $< +firmware=upd3reaker_fw.hex

upd3synsim: upd3reaker_syn_tb.vvp upd3reaker_fw.hex
	vvp -N $< +firmware=upd3reaker_fw.hex

upduino3.json: upduino3.v ice40up5k_spram.v spimemio.v simpleuart.v picosoc.v ../picorv32.v
	yosys -ql upduino3.log -p 'synth_ice40 -top upduino3 -json upduino3.json' $^

upduino3_tb.vvp: upduino3_tb.v upduino3.v ice40up5k_spram.v spimemio.v simpleuart.v picosoc.v ../picorv32.v spiflash.v
	iverilog -s testbench -o $@ $^ `yosys-config --datdir/ice40/cells_sim.v`

upduino3_syn_tb.vvp: upduino3_tb.v upduino3_syn.v spiflash.v
	iverilog -s testbench -o $@ $^ `yosys-config --datdir/ice40/cells_sim.v`

upduino3_syn.v: upduino3.json
	yosys -p 'read_json upduino3.json; write_verilog upduino3_syn.v'

upduino3.asc: upduino3.pcf upduino3.json
	nextpnr-ice40 --freq 13 --up5k --asc upduino3.asc --pcf upduino3.pcf --json upduino3.json

upduino3.bin: upduino3.asc
	icetime -d up5k -c 12 -mtr upduino3.rpt upduino3.asc
	icepack upduino3.asc upduino3.bin

upd3prog: upduino3.bin upduino3_fw.bin
	iceprog upduino3.bin
	iceprog -o 1M upduino3_fw.bin

upd3prog_fw: upduino3_fw.bin
	iceprog -o 1M upduino3_fw.bin

upduino3_sections.lds: sections.lds
	$(CROSS)cpp -P -DUPDUINO -o $@ $^

upduino3_fw.elf: upduino3_sections.lds start.s firmware.c
	$(CROSS)gcc $(CFLAGS) -DUPDUINO -march=rv32ic -Wl,-Bstatic,-T,upduino3_sections.lds,--strip-debug -ffreestanding -nostdlib -o upduino3_fw.elf start.s firmware.c

upduino3_fw.hex: upduino3_fw.elf
	$(CROSS)objcopy -O verilog upduino3_fw.elf upduino3_fw.hex

upduino3_fw.bin: upduino3_fw.elf
	$(CROSS)objcopy -O binary upduino3_fw.elf upduino3_fw.bin

# ---- iCE40 MCH2022 V2 Board ----

mch2sim: mch2reaker_tb.vvp mch2reaker_fw.hex
	vvp -N $< +firmware=mch2reaker_fw.hex

mch2synsim: mch2reaker_syn_tb.vvp mch2reaker_fw.hex
	vvp -N $< +firmware=mch2reaker_fw.hex

mch2022v2.json: mch2022v2.v ice40up5k_spram.v spimemio.v simpleuart.v picosoc.v ../picorv32.v
	yosys -ql mch2022v2.log -p 'synth_ice40 -top mch2022v2 -json mch2022v2.json' $^

mch2022v2_tb.vvp: mch2022v2_tb.v mch2022v2.v ice40up5k_spram.v spimemio.v simpleuart.v picosoc.v ../picorv32.v spiflash.v
	iverilog -s testbench -o $@ $^ `yosys-config --datdir/ice40/cells_sim.v`

mch2022v2_syn_tb.vvp: mch2022v2_tb.v mch2022v2_syn.v spiflash.v
	iverilog -s testbench -o $@ $^ `yosys-config --datdir/ice40/cells_sim.v`

mch2022v2_syn.v: mch2022v2.json
	yosys -p 'read_json mch2022v2.json; write_verilog mch2022v2_syn.v'

mch2022v2.asc: mch2022v2.pcf mch2022v2.json
	nextpnr-ice40 --freq 13 --up5k --asc mch2022v2.asc --pcf mch2022v2.pcf --json mch2022v2.json

mch2022v2.bin: mch2022v2.asc
	icetime -d up5k -c 16 -mtr mch2022v2.rpt mch2022v2.asc
	icepack mch2022v2.asc mch2022v2.bin

mch2prog: mch2022v2.bin mch2022v2_fw.bin
	iceprog mch2022v2.bin
	iceprog -o 1M mch2022v2_fw.bin

mch2prog_fw: mch2022v2_fw.bin
	iceprog -o 1M mch2022v2_fw.bin

mch2022v2_sections.lds: sections.lds
	$(CROSS)cpp -P -DUPDUINO -o $@ $^

mch2022v2_fw.elf: mch2022v2_sections.lds start.s firmware.c
	$(CROSS)gcc $(CFLAGS) -DUPDUINO -march=rv32ic -Wl,-Bstatic,-T,mch2022v2_sections.lds,--strip-debug -ffreestanding -nostdlib -o mch2022v2_fw.elf start.s firmware.c

mch2022v2_fw.hex: mch2022v2_fw.elf
	$(CROSS)objcopy -O verilog mch2022v2_fw.elf mch2022v2_fw.hex

mch2022v2_fw.bin: mch2022v2_fw.elf
	$(CROSS)objcopy -O binary mch2022v2_fw.elf mch2022v2_fw.bin

# ---- Testbench for SPI Flash Model ----

spiflash_tb: spiflash_tb.vvp firmware.hex
	vvp -N $<

spiflash_tb.vvp: spiflash.v spiflash_tb.v
	iverilog -s testbench -o $@ $^

# ---- ASIC Synthesis Tests ----

cmos.log: spimemio.v simpleuart.v picosoc.v ../picorv32.v
	yosys -l cmos.log -p 'synth -top picosoc; abc -g cmos2; opt -fast; stat' $^

# ---- Clean ----

clean:
	rm -f testbench.vvp testbench.vcd spiflash_tb.vvp spiflash_tb.vcd
	rm -f hx8kdemo_fw.elf hx8kdemo_fw.hex hx8kdemo_fw.bin cmos.log
	rm -f icebreaker_fw.elf icebreaker_fw.hex icebreaker_fw.bin
	rm -f hx8kdemo.blif hx8kdemo.log hx8kdemo.asc hx8kdemo.rpt hx8kdemo.bin
	rm -f hx8kdemo_syn.v hx8kdemo_syn_tb.vvp hx8kdemo_tb.vvp
	rm -f icebreaker.json icebreaker.log icebreaker.asc icebreaker.rpt icebreaker.bin
	rm -f icebreaker_syn.v icebreaker_syn_tb.vvp icebreaker_tb.vvp
	rm -f upduinov3.json upduinov3.log upduinov3.asc upduinov3.rpt upduinov3.bin
	rm -f upduinov3_syn.v upduinov3_syn_tb.vvp upduinov3_tb.vvp

	rm -f mch2022v2.json mch2022v2.log mch2022v2.asc mch2022v2.rpt mch2022v2.bin
	rm -f mch2022v2_syn.v mch2022v2_syn_tb.vvp mch2022v2_tb.vvp

.PHONY: spiflash_tb clean
.PHONY: hx8kprog hx8kprog_fw hx8ksim hx8ksynsim
.PHONY: icebprog icebprog_fw icebsim icebsynsim
