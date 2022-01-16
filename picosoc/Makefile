
CROSS=riscv32-unknown-elf-
CFLAGS=

# ---- Testbench for SPI Flash Model ----

spiflash_tb: spiflash_tb.vvp firmware.hex
	vvp -N $<

spiflash_tb.vvp: spiflash.v spiflash_tb.v
	iverilog -s testbench -o $@ $^

# --- MCH2022V2 Firmware ---
all: mch2022v2.bin mch2022v2_fw.bin

mch2sim: mch2022v2_tb.vvp mch2022v2_fw.hex
	vvp -N $< +firmware=mch2022v2_fw.hex

mch2synsim: mch2reaker_syn_tb.vvp mch2022v2_fw.hex
	vvp -N $< +firmware=mch2022v2_fw.hex

mch2022v2.json: mch2022v2.v ice40up5k_spram.v spipsramio.v simpleuart.v picosoc.v ../picorv32.v
	yosys -ql mch2022v2.log -p 'synth_ice40 -top mch2022v2 -json mch2022v2.json' $^

mch2022v2_tb.vvp: mch2022v2_tb.v mch2022v2.v ice40up5k_spram.v spipsrammio.v simpleuart.v picosoc.v ../picorv32.v spiflash.v
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
	$(CROSS)cpp -P -DMCH2022V2 -o $@ $^

mch2022v2_fw.elf: mch2022v2_sections.lds start.s firmware.c
	$(CROSS)gcc $(CFLAGS) -DMCH2022V2 -march=rv32ic -Wl,-Bstatic,-T,mch2022v2_sections.lds,--strip-debug -ffreestanding -nostdlib -o mch2022v2_fw.elf start.s firmware.c

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

	rm -f mch2022v2.json mch2022v2.log mch2022v2.asc mch2022v2.rpt mch2022v2.bin
	rm -f mch2022v2_syn.v mch2022v2_syn_tb.vvp mch2022v2_tb.vvp

.PHONY: spiflash_tb clean all
