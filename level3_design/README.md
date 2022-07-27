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
