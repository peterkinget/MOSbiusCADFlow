# MOSbiusV2Tools

Tools for the MOSbiusV2. 

## Circuit Description

### Regular-Bus Connections

There are 8 regular buses ("RBUS"); the `.json` circuit file describes which pins connect to each
```
{
    "RBUS1": ["DINV2_INP_L", "DINV2_INN_L"],
    "RBUS2": ["DINV2_OUT_L", "DINV2_INP_R", "DINV2_INN_R"],
    "RBUS3": ["DINV2_OUT_R", "DINV1_INP_L", "DINV1_INN_L"],
    "RBUS4": ["DINV1_OUT_L", "DINV1_INP_R", "DINV1_INN_R"], 

}
```


### Switched-Bus Connections

### Transistor Sizing

Create a `.json` file with the sizing for all the devices; here is an empty file:
```
{
    "CC_N": [],
    "CC_P": [],
    "DCC1_N_L": [],
    "DCC1_N_R": [],
    "DCC1_P_L": [],
    "DCC1_P_R": [],
    "DCC2_N_L": [],
    "DCC2_N_R": [],
    "DCC2_P_L": [],
    "DCC2_P_R": [],
    "DCC3_N_L": [],
    "DCC3_N_R": [],
    "DCC3_P_L": [],
    "DCC3_P_R": [],
    "DCC4_N_L": [],
    "DCC4_N_R": [],
    "DCC4_P_L": [],
    "DCC4_P_R": [],
    "DINV1_L": [],
    "DINV1_R": [],
    "DINV2_L": [],
    "DINV2_R": [],
    "OTA_N": [],
    "OTA_P": []
}
``` 
Fill in the sizes `0, 1, 2, ... 31` for the respective devices in the file. If you omit a device the size will be set to `0`. Here is an example of a sizing file: 
```
{
    "CC_N": [1],
    "CC_P": [1],
    "DCC1_N_L": [5],
    "DCC1_N_R": [5],
    "DCC1_P_L": [5],
    "DCC1_P_R": [5],
    "DCC2_N_L": [7],
    "DCC2_N_R": [7],
    "DCC2_P_L": [7],
    "DCC2_P_R": [7],
    "DCC3_N_L": [9],
    "DCC3_N_R": [9],
    "DCC3_P_L": [9],
    "DCC3_P_R": [9],
    "DCC4_N_L": [11],
    "DCC4_N_R": [11],
    "DCC4_P_L": [11],
    "DCC4_P_R": [11],
    "DINV1_L": [13],
    "DINV1_R": [13],
    "DINV2_L": [15],
    "DINV2_R": [15],
    "OTA_N": [1],
    "OTA_P": [1]
}
```

