import streamlit as st


class StProgress:
    def __init__(self, iterable, title=None):
        self.title_text = title
        if self.title_text is None:
            self.title_text = "Processed "
        else:
            self.title_text += " "

        self.prog_bar = st.progress(0)
        self.iterable = iterable
        self.length = len(iterable)
        self.i = 0

    def __iter__(self):
        for obj in self.iterable:
            yield obj
            self.i += 1
            current_prog = self.i / self.length
            self.prog_bar.progress(current_prog)
            print(self.title_text + str(self.i) + " / " + str(self.length))
