# Verification of ALU

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![image](https://user-images.githubusercontent.com/74342939/181232897-685da6c8-38be-4efa-a30f-c18a15339673.png)

## Design Description

- ALU(Arthimetic logic unit) is designed in such a way that it contains two sub blocks in it namely Arthimetic unit and logical unit.
- Arthimetic unit does the operations like Addition , Subtraction , Multiplication , Division.
- Logical unit does all the logical operations like AND , OR , NAND , NOR.
- It also has CLK and RSTN(Asynchronous low) signals for controlling the operations.
- It has an other signal called OPCODE. Various operations are performed based on the value of opcode given.
```
Opcode values and its respective operation:
0 - ADDITION
1 - SUBTRACTION
2 - PRODUCT
3 - DIVISION
4 - LOGICAL_OR
5 - LOGICAL_AND
6 - LOGICAL_NAND
7 - LOGICAL_NOR
```

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (alu module) which takes three inputs, in1 and in2 of 5-bit (MSB is signed bit) width and opcode as 3-bit width. It has clk and rstn as 1-bit inputs. It also has an output of 9-bit (MSB is signed bit) which generates the output of the respective performed.

## Verification without bug insertion

The values are assigned to the inputs using
```
dut.in1.value = A
dut.in2.value = B
dut.opcode.value = C
await FallingEdge(dut.clk)
```
- All the inputs are driven at the Falling Edge of the clock, so that they are stable and readily available when the Rising Edge of clock is seen.

The assert statement is used for comparing the design's outut to the expected value.

The following error is seen:
```
assert dut.out_top.value == A+B, "Test1 failed with: in1={A} , in2={B} , opcode={C} , DUT_OUT={D}".format(A=dut.in1.value, B=dut.in2.value, C=dut.opcode.value, D=dut.out_top.value)
```

Test is simulated without inserting bugs:
![image](https://user-images.githubusercontent.com/74342939/181241517-5e26b499-8194-419a-9da6-374d833e0bb8.png)

### Test Scenario - 1 (Passed)
- Test Inputs: in1 = 05 , in2 = 10 , opcode = 0 (Addition)
- Expected Output: out = 15
- DUT Output: out = 15

### Test Scenario - 2 (Passed)
- Test Inputs: in1 = 04 , in2 = 02 , opcode = 1 (Subtraction)
- Expected Output: out = 02
- DUT Output: out = 02

## Bug Insertion
Bug is inserted in adder and subtractor modules as shown below:
```
//adder
module add(in1 , in2 , out_add);
  
  input signed [4:0]in1;
  input signed [4:0]in2;
  output signed [8:0]out_add;
  
  assign out_add = in1 - in2;     =======>bug-1 is inserted. It should actually be as (out_add = in1 + in2)
  
endmodule
```

```
//subtractor
module subtract(in1 , in2 , out_sub);
  
  input signed [4:0]in1;
  input signed [4:0]in2;
  output signed [8:0]out_sub;
  
  assign out_sub = in1 * in2;     =======>bug-2 is inserted. It should actually be as (out_add = in1 - in2)
  
endmodule
```

- In the first bug when the opcode is 0, it should perform addition. After bug insertion it behaves as subtractor.
- In the second bug when the opcode is 1, it should perform subtraction. After bug insertion it behaves as multiplier.

### Test Scenario - 1 (Failed)
- Test Inputs: in1 = 10 , in2 = 5 , opcode = 0 (Addition)
- Expected Output: out = 15
- DUT Output: out = 05
- Here, Subtraction is performed instead of Addition
### Test Scenario - 2 (Failed)
- Test Inputs: in1 = 04 , in2 = 02 , opcode = 1 (Subtraction)
- Expected Output: out = 02
- DUT Output: out = 08
- Here, Multiplication is done instead of Subtraction

Test is simulated after inserting bugs into the design:
![image](https://user-images.githubusercontent.com/74342939/181241992-8bc6970e-a85a-4d93-8d04-72fe6d05f6dc.png)

## Verification Strategy
I developed different testcases for alu design before and after inserting bugs. By developing different testcases it is easy to debug the bugs.
