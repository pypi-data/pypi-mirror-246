[![Open in Huggingface](https://huggingface.co/datasets/huggingface/badges/raw/refs%2Fpr%2F11/open-in-hf-spaces-md-dark.svg)](https://huggingface.co/spaces/z-uo/SweetHome3DPlanner)

# Streamlit SweetHome3D
This project have the aim to port an house planner to streamlit in order to use it as a component of some demos including a good view with basic features quickly.

![example of UI](https://gitlab.com/nicolalandro/streamlit-sweethome3d/-/raw/main/examples/imgs/screen.png)

```
import streamlit as st
from streamlit_sweethome3d import streamlit_sweethome3d

# if you want to use wide screen to see more buttons
# st.set_page_config(layout="wide")

import json

in_state = {
    "homes": [
      {
        "walls": [
          [0, 180, 0, 400, 20, 250], # params: x1, y1 x2, y2, spessore, altezza
          [350, 180, 350, 400, 20, 250],
          [0-10, 180, 350+10, 180, 20, 250]
        ],
        "rooms": [
          [[0,180], [350, 180], [350, 400], [0, 400]] # points
        ],
        "furnitures": [
          {
            "id": "eTeks#shower", # https://gitlab.com/nicolalandro/streamlit-sweethome3d/-/blob/main/FURNITURE_DOC.md
            "x": 50,
            "y": 230,
            "elevation": 0,
          }
        ]
      }
    ]
}

out_state = streamlit_sweethome3d(state = in_state, out_state=True)

col1, col2 = st.columns(2)
with col1:
    st.text('in state')
    st.code(json.dumps(in_state, indent=1))
with col2:
    st.text('out state')
    st.code(json.dumps(out_state, indent=1))
```
