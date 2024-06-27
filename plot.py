# import streamlit as st
# import numpy as np
# import plotly.graph_objects as go
# from scipy.stats import weibull_min


# def plot_interactive_weibull(ttf_data):
#     mean_ttf = np.mean(ttf_data)
#     shape, loc, scale = weibull_min.fit(ttf_data, floc=0)
#     scale = mean_ttf / np.math.gamma(1 + 1 / shape)
#     fr = 1 / ttf_data
#     shape = 1 / np.std(np.log(fr))

#     x = np.linspace(min(ttf_data), max(ttf_data), 10000)
#     pdf_values = (shape / scale) * (x / scale)**(shape - 1) * np.exp(-((x / scale)**shape))
#     hazard_function = pdf_values / (1 - np.exp(-((x / scale)**shape)))

#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=x, y=pdf_values, mode='lines', name='Weibull Distribution'))
#     fig.add_trace(go.Scatter(x=ttf_data, y=np.zeros_like(ttf_data), mode='markers', marker=dict(color='red'), name='TTF Data'))
#     fig.add_trace(go.Scatter(x=x, y=hazard_function, mode='lines', name='Hazard Function', line=dict(dash='dash')))
#     fig.update_layout(title='Grafik Weibull Distribution, Hazard Function, dan TTF Data',
#                       xaxis_title='Time-to-Failure (TTF)',
#                       yaxis_title='Probability Density / Hazard Function',
#                       legend=dict(
#                           orientation="h",
#                           yanchor="bottom",
#                           y=1.02,
#                           xanchor="right",
#                           x=1
#                       ))
#     st.plotly_chart(fig, use_container_width=True)
#     st.write("Weibull Parameters:")
#     st.write(f"Shape (c): {shape:.4f}")
#     st.write(f"Location (loc): {loc:.4f}")
#     st.write(f"Scale (scale): {scale:.4f}")

import streamlit as st
import numpy as np
import plotly.graph_objects as go
from scipy.stats import weibull_min
import math

def plot_interactive_weibull(ttf_data):
    mean_ttf = np.mean(ttf_data)
    
    # Fit Weibull distribution
    shape, loc, scale = weibull_min.fit(ttf_data, floc=0)
    scale = mean_ttf / math.gamma(1 + 1 / shape)
    
    # Calculate Failure Rate
    fr = 1 / ttf_data
    shape = 1 / np.std(np.log(fr))
    
    # Create data for plotting
    x = np.linspace(min(ttf_data), max(ttf_data), 10000)
    pdf_values = weibull_min.pdf(x, shape, loc, scale)
    hazard_function = pdf_values / (1 - weibull_min.cdf(x, shape, loc, scale))
    
    # Create plot
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=pdf_values, mode='lines', name='Weibull Distribution'))
    fig.add_trace(go.Scatter(x=ttf_data, y=np.zeros_like(ttf_data), mode='markers', marker=dict(color='red'), name='TTF Data'))
    fig.add_trace(go.Scatter(x=x, y=hazard_function, mode='lines', name='Hazard Function', line=dict(dash='dash')))
    
    fig.update_layout(
        title='Grafik Weibull Distribution, Hazard Function, dan TTF Data',
        xaxis_title='Time-to-Failure (TTF)',
        yaxis_title='Probability Density / Hazard Function',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )
    
    st.plotly_chart(fig, use_container_width=True)
    st.write("Weibull Parameters:")
    st.write(f"Shape (c): {shape:.4f}")
    st.write(f"Location (loc): {loc:.4f}")
    st.write(f"Scale (scale): {scale:.4f}")


