# Verification of Multiplexer

The verification environment is setup using [Vyoma's UpTickPro](https://vyomasystems.com) provided for the hackathon.

![image](https://user-images.githubusercontent.com/74342939/180381197-de069a66-7b03-4d81-ad06-f12f24fe419a.png)

## Verification Environment

The [CoCoTb](https://www.cocotb.org/) based Python test is developed as explained. The test drives inputs to the Design Under Test (multiplexer module) which takes in 31 2-bit inputs and a 5-bit select-line as an input which selects the input based on the select-line and drives the correspondent input to the output. 

The values are assigned to the input ports using
```
dut.inp1.value = 3
dut.sel.value = 1
```

The assert statement is used for comparing the adder's outut to the expected value.

The following error is seen:
```
assert dut.out.value == A, "Test1 failed with: sel={A} , expected_out={B} , DUT_OUT={C}".format(A=dut.sel.value, B=dut.inp13.value, C=dut.out.value)
```
## Test Scenario - 1 (Passed)
- Test Inputs: inp0 = 03 , sel = 0
- Expected Output: out = 03
- DUT Output: out = 03

Output matches for the above inputs provided.
## Test Scenario - 2 (Failed)
- Test Inputs: inp12 = 02 , sel = 12
- Expected Output: out = 02
- DUT Output: out = 00

Output mismatches for the above inputs proving that there is a design bug.
## Test Scenario - 3 (Failed)
- Test Inputs: inp13 = 03 , sel = 13
- Expected Output: out = 03
- DUT Output: out = 'z'

Output mismatches for the above inputs proving that there is a design bug.

## Design Bug
Based on the above test inputs and analysing the design, we see the following

```
always@(*)
  begin
    case(sel)
      .
      .
      .
      5'b01101: out = inp12;       =======>BUG   
      5'b01101: out = inp13;       =======>BUG
      .
      .
      endcase
    end
```

## Design fix and explanation of bugs
Explanation:

- When the select line is 12 (sel = 12), the design doesn't have a case for it. So the input is not driven and the output remains 0.
- When the select line is 13 (sel = 13), the design have two cases in it. So the design doesn't know which case to pick. So the output is High Impedance (z).

Design Fix:

- When we include a case for sel = 12 and remove extra case for sel = 13 the the bugs are removed.
```
always@(*)
  begin
    case(sel)
      .
      .
      .
      5'b01100: out = inp12;       =======>bug fixed  
      5'b01101: out = inp13;       =======>bug fixed
      .
      .
      endcase
    end
```

![image](https://user-images.githubusercontent.com/74342939/180392449-33998425-a588-40c2-b121-41b571813267.png)
