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

