import os
import streamlit.components.v1 as components

_RELEASE = os.getenv('_RELEASE_STREAMLIT_SWEETHOME_3D', "1")

if _RELEASE == "0":
  _component_func = components.declare_component(
    "sweethome3d_component",
    url="http://localhost:5173", # vite dev server port
  )
else:
  parent_dir = os.path.dirname(os.path.abspath(__file__))
  build_dir = os.path.join(parent_dir, "frontend/dist")
  _component_func = components.declare_component("sweethome3d_component", path=build_dir)

def streamlit_sweethome3d(state, out_state=False, key=None):
  component_value = _component_func(state=state, out_state=out_state, key=key, default=0)
  return component_value

if _RELEASE == "0":
  import json
  import streamlit as st
  # st.set_page_config(layout="wide",)
  st.subheader("Component Test")

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
            "id": "eTeks#shower",
            "x": 50,
            "y": 230,
            "elevation": 0,
          }
        ]
      }
    ]
  }

  out_state = streamlit_sweethome3d(state = in_state, out_state = True)

  col1, col2 = st.columns(2)
  with col1:
      st.text('in state')
      st.code(json.dumps(in_state, indent=2))
  with col2:
      st.text('out state')
      st.code(json.dumps(out_state, indent=2))
