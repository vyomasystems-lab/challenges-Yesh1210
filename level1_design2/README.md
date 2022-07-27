# Verification of Sequence Detector (1011)

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![image](https://user-images.githubusercontent.com/74342939/181215506-7d8d5a75-d014-488d-9be1-92fb9cdcfd4d.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (sequence detector module) which takes in 1-bit input along with clock and reset signals. It also has an output of 1-bit which is asserted when the sequence (1011) is detected.

In this design all the inputs are generated at the Falling Edge of the clock, so that they are stable when the Rising Edge of clock is seen.

The values are assigned to the input ports using
```
dut.inp_bit.value = 1
await FallingEdge(dut.clk)
dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)
```

The assert statement is used for comparing the adder's outut to the expected value.

The following error is seen:
```
assert dut.seq_seen.value == 1, f"Test failed with {dut.seq_seen.value} != 1"
```

## Test Scenario - 1 (Failed)
```
dut.inp_bit.value = 1
await FallingEdge(dut.clk)
dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

dut.inp_bit.value = 0
await FallingEdge(dut.clk)
dut._log.info("after receiving 0 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

dut.inp_bit.value = 1
await FallingEdge(dut.clk)
dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

dut.inp_bit.value = 1
await FallingEdge(dut.clk)
dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

dut.inp_bit.value = 0
await FallingEdge(dut.clk)
dut._log.info("after receiving 0 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

dut.inp_bit.value = 1
await FallingEdge(dut.clk)
dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

dut.inp_bit.value = 1
await FallingEdge(dut.clk)
dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)
```
- For a given sequence the output is high only for some bits. It is also not overlapped. 

![image](https://user-images.githubusercontent.com/74342939/181218791-3dcfb34b-c708-45d7-aac2-56bd1ece6c57.png)

## Test Scenario - 2 (Failed)
```
#dut.inp_bit.value = 1
await FallingEdge(dut.clk)
dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

dut.inp_bit.value = 1
await FallingEdge(dut.clk)
dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

dut.inp_bit.value = 0
await FallingEdge(dut.clk)
dut._log.info("after receiving 0 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

dut.inp_bit.value = 1
await FallingEdge(dut.clk)
dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)

dut.inp_bit.value = 1
await FallingEdge(dut.clk)
dut._log.info("after receiving 1 current_state = %s, seq_seen = %s", dut.current_state.value , dut.seq_seen.value)
```
- When the fisrt bit is different and then the required sequence of bits is given it doesn't detect it.

![image](https://user-images.githubusercontent.com/74342939/181219126-f52dd7cc-6f27-439d-98d2-67df81279912.png)

## Design Bugs
```
case(current_state)
      IDLE:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = IDLE;         
      end
      SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = IDLE;           =======>BUG
        else
          next_state = SEQ_10;
      end
      SEQ_10:
      begin
        if(inp_bit == 1)
          next_state = SEQ_101;
        else
          next_state = IDLE;
      end
      SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = IDLE;            =======>BUG
      end
      SEQ_1011:
      begin
        next_state = IDLE;              =======>BUG
      end
    endcase
```

## Design fix
- When we make the following changes in the code the sequence (1011) with overlapped model is detected
```
case(current_state)
      IDLE:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = IDLE;         
      end
      SEQ_1:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;           =======>bug fixed
        else
          next_state = SEQ_10;
      end
      SEQ_10:
      begin
        if(inp_bit == 1)
          next_state = SEQ_101;
        else
          next_state = IDLE;
      end
      SEQ_101:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1011;
        else
          next_state = SEQ_10;            =======>bug fixed
      end
      SEQ_1011:
      begin
        if(inp_bit == 1)
          next_state = SEQ_1;
        else
          next_state = SEQ_10;            =======>bug fixed
      end
    endcase
```

![image](https://user-images.githubusercontent.com/74342939/181223571-d9e82fc1-a619-4e2b-b19d-9f001afac6fd.png)

The updated design is checked in as seq_detect_1011_fixed.v

## Verification Strategy

I created a variety of testcases with different types of inputs to check for the sequence detection and overlapping model. It will be simple to debug into it by creating various scenarios.
