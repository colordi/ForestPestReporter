import streamlit
import streamlit.web.bootstrap as bootstrap

if __name__ == '__main__':
    streamlit._is_running_with_streamlit = True
    bootstrap.run('主页.py', 'streamlit run', (), {})