import time
from streamlit import button, columns, fragment, metric, rerun, session_state, sidebar, write
def start_timer():
    if not session_state.running:
        session_state.running = True
        session_state.start_time = time.time() - session_state.elapsed_time
def stop_timer():
    if session_state.running:
        session_state.running = False
        session_state.elapsed_time = time.time() - session_state.start_time
def reset_timer():
    session_state.running = False
    session_state.start_time = None
    session_state.elapsed_time = 0
@fragment(run_every=0.4)
def timer():
    if 'running' not in session_state:
        session_state.running = False
    if 'start_time' not in session_state:
        session_state.start_time = None
    if 'elapsed_time' not in session_state:
        session_state.elapsed_time = 0
    if session_state.running:
        session_state.elapsed_time = time.time() - session_state.start_time
    elapsed_minutes = int(session_state.elapsed_time // 60)
    elapsed_seconds = int(session_state.elapsed_time % 60)
    metric(
                label="Timer:",
                value=f"{elapsed_minutes} min",
                delta=f"{elapsed_seconds} s",
                help="Minutes:Seconds",
                label_visibility="collapsed",
            )
    col1, col2 = columns(2, gap="small")
    icon = "❚❚" if session_state.running else "▶"
    with col1:
        if button(label=icon, use_container_width=True):
            if not session_state.running:
                start_timer()
            else:
                stop_timer()
                rerun()
    with col2:
        if button("⏹", use_container_width=True, disabled=session_state.elapsed_time==0 or session_state.running):
            reset_timer()
