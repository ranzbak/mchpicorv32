`default_nettype none

module passthrough (
        output wire    [2:0] led,
        output wire          uart_tx,
        input  wire          uart_rx,
        output wire          spi_esp32_miso,
        input  wire          spi_esp32_mosi,
        input  wire          spi_esp32_sck,
        input  wire          spi_esp32_cs,
        input  wire          spi_ram_data1,
        output wire          spi_ram_data0,
        output wire          spi_ram_data2,
        output wire          spi_ram_data3,
        output wire          spi_ram_sck,
        output wire          spi_ram_cs
    );

    // PSRAM passthrough
    assign spi_esp32_miso = spi_ram_data1;
    assign spi_ram_data0 = spi_esp32_mosi;
    assign spi_ram_cs = spi_esp32_cs;
    assign spi_ram_sck = spi_esp32_sck;
    assign spi_ram_data2 = 1'b1;
    assign spi_ram_data3 = 1'b1;

    // UART loopback
    assign uart_tx = uart_rx;

    // LED
    wire LED_R, LED_G, LED_B;

    assign LED_R = 1'b1;
    assign LED_G = spi_esp32_cs;
    assign LED_B = 1'b1;

    // RGB IP
    SB_RGBA_DRV #(
                    .CURRENT_MODE("0b1"),
                    .RGB0_CURRENT("0b000001"),
                    .RGB1_CURRENT("0b000001"),
                    .RGB2_CURRENT("0b000001")
                ) u_rgb_drv (
                    .RGB0(led[0]),
                    .RGB1(led[1]),
                    .RGB2(led[2]),
                    .RGBLEDEN(1'b1),
                    .RGB0PWM(spi_esp32_cs),
                    .RGB1PWM(!spi_esp32_cs),
                    .RGB2PWM(0),
                    .CURREN(1'b1)
                );

endmodule
